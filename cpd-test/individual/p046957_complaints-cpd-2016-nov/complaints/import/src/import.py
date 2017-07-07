import os
import sys
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

inv_df.to_csv("../output/" + "investigators.csv" , index = False)
