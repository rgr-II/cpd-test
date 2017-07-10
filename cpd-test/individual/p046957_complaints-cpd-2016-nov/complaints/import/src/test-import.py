import re
import os
import sys
import io
import numpy as np
import pandas as pd
from operator import itemgetter
import datetime
import itertools

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)
from helperfunctions import *

input_path = "../input/"
out_path = "../output/"
outname = "complaints.csv"
files = [input_path + f for f in os.listdir(input_path)]

f = files[0]

df = pd.read_excel(f, rows = 20)
col_list = df.columns.tolist()
Report_Produced_Date = [x for x in col_list if isinstance(x, datetime.datetime)]
col_list = [x for x in col_list if x not in Report_Produced_Date]
FOIA_Request = [x for x in col_list if 'FOIA' in x][0]
skip = np.where(df.iloc[:,0]=='Number:')[0][0]+1

df = pd.read_excel(f, skiprows = skip)
df.dropna(how='all', inplace=True)
df.dropna(subset=['Number:', 'Beat:', 'Location Code:', 'Address of Incident:', 'Unnamed: 6', 'Incident Date & Time', 'Complaint Date', 'Closed Date'], how='all', axis=0)

df['Number:'].fillna(method='ffill', inplace=True)
df['Number:'] = df['Number:'].astype(int)

df1 = df[
            df['Incident Date & Time'].isnull() &
            df['Complaint Date'].isnull() &
            df['Closed Date'].isnull()].loc[:, ('Number:', 'Location Code:',
                                                'Address of Incident:','Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6')]
df1.columns = ['Number:', 'Investigator:', 'Assignment', 'Rank', 'Star', 'Appt_Date']

df2 = df.merge(df1, how='left',on='Number:')

df2.dropna(subset = ['Incident Date & Time', 'Complaint Date', 'Closed Date'], how='all', axis=0, inplace=True)

buf = io.StringIO()
df2.info(buf=buf)
s = buf.getvalue()
info_values = [re.split("\\s\\s+", x) for x in s.split("\n")]
info_values = [x for x in info_values if len(x)>1]
info_values = [x[0] for x in info_values if x[1].startswith('0 non-null')]
#print(df2.dropna(how='all', axis=1).equals(df2.drop(info_values, 1)))
df2 = df2.dropna(how='all', axis=1)

df2['Address of Incident:'] = df2['Address of Incident:'].astype(str)
df2['Unnamed: 4'] = df2['Unnamed: 4'].astype(str)
df2['Unnamed: 5'] = df2['Unnamed: 5'].astype(str)
df2['Unnamed: 6'] = df2['Unnamed: 6'].astype(str)

df2['Address of Incident:'] = (df2[['Address of Incident:', 'Unnamed: 4', 'Unnamed: 5']]
                                .apply(lambda x: ' '.join(x), axis=1)
                                .str.replace("nan", "")
                                .str.strip())
df2 = df2[["Number:", "Beat:", "Location Code:", "Address of Incident:", "Unnamed: 6", "Incident Date & Time", "Complaint Date", "Closed Date", "Investigator:", "Assignment", "Rank", "Star", "Appt_Date"]]

df2.columns = ["CRID", "Beat", "Location_Code", "Address_of_Incident", "City_State_Zip", "Incident_Date", "Complaint_Date", "Closed_Date", "Investigator_Full_Name", "Investigator_Assignment", "Investigator_Rank", "Investigator_Star", "Investigator_Appt_Date"]

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

new_states_list = []
for value in df2["City_State_Zip"][:30]:
    #print("****")
    #print(value)
    if hasNumbers(value):
        split_state = value.split(" ")
        #print(split_state)
        while len(split_state)>3:
            split_state = [split_state[0] + ' ' + split_state[1]]+split_state[2:]
            print(split_state)
    else:
        split_state = value.split(" ")
        while len(split_state)>2:
            split_state = [split_state[0] + ' ' + split_state[1]] + split_state[2:]
            #print(split_state)
    new_states_list.append(split_state)
city_state_zip = pd.DataFrame(new_states_list)
city_state_zip.columns = ["City", "State", "Zip"]
df2 = df2.merge(city_state_zip, how='left', right_index=True, left_index=True)
df2 = df2[["CRID", "Beat", "Location_Code", "Address_of_Incident", "City", "State", "Zip", "Incident_Date", "Complaint_Date", "Closed_Date", "Investigator_Full_Name", "Investigator_Assignment", "Investigator_Rank", "Investigator_Star", "Investigator_Appt_Date"]]
df2["FOIA_Request_Number"]=FOIA_Request
try: df["Report_Produced_Date"] = Report_Produced_Dated.date()
except: df["Report_Produced_Date"]=''

# metadata_dataset
metadata_df = pd.DataFrame()
buf = io.StringIO()
df2.info(buf=buf)
s = buf.getvalue()
info_values = [re.split("\\s\\s+",x) for x in s.split("\n")]
info_values = [x for x in info_values if len(x)>1]
metadata_df = pd.DataFrame(info_values)
metadata_df["File"] = f
metadata_df.columns = ["Column_Name", "Column_Info", "Original_Dataset"]
metadata_df["Non_Null_Count"], metadata_df["Object_Type"] = metadata_df["Column_Info"].str.split(" ", 1).str
metadata_df["Object_Type"] = metadata_df["Object_Type"].str.replace("non-null", "")
uniques_df = df2.apply(lambda x: len(x.unique())).reset_index()
uniques_df.columns = ["Column_Name", "Unique_Count"]
metadata_df["Unique_Count"] = uniques_df["Unique_Count"]
print(metadata_df.head())
'''
data = pd.DataFrame()

for f in files:
    df = ReadMessy(f)
    data = (data
            .append(df)
            .reset_index(drop=True))

data.insert(0, "CRID", (data["Number:"]
                        .fillna(method='ffill')
                        .astype(int)))

cmpl_df = (data[~data["Number:"].isnull()]
            .dropna(how='all', axis=0)
            .dropna(how='all',axis=1)
            .drop('Number:', axis=1))

cmpl_df.columns = ["CRID", "Beat", "Location_Code", "Address_Number", "Street", "Apartment_Number", "City_State", "Incident_Datetime", "Complaint_Date", "Closed_Date"]

cmpl_df.to_csv("../output/" + "complaints.csv" , index = False)

inv_df = (data[data["Number:"].isnull()]
            .dropna(how='all', axis=0)
            .dropna(how='all',axis=1)
            .drop('Beat:', axis=1))

inv_df.columns = ["CRID", "Full_Name", "Assignment", "Rank", "Star", "Appointed_Datetime"]

inv_df.to_csv("../output/" + "investigators.csv" , index = False)'''
