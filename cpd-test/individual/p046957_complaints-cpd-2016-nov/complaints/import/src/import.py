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
from utils import *

input_path = "../input/"
out_path = "../output/"
outname = "complaints.csv"
files = [input_path + f for f in os.listdir(input_path)]

cmpl_data = pd.DataFrame()
cmpl_metadata = pd.DataFrame()
cmpl_out = "complaints.csv"

inv_data = pd.DataFrame()
inv_metadata = pd.DataFrame()
inv_out = "investigators.csv"

for f in files:
    df = ReadMessy(f)
    df.insert(0, "CRID", (df["Number:"]
                            .fillna(method='ffill')
                            .astype(int)))
    cmpl_df = (df[~df["Number:"].isnull()]
                .dropna(how='all', axis=0)
                .dropna(how='all',axis=1)
                .drop('Number:', axis=1))

    cmpl_df.columns = ["CRID", "Beat", "Location_Code", "Address_Number", "Street", "Apartment_Number", "City_State", "Incident_Datetime", "Complaint_Date", "Closed_Date"]
    cmpl_data = (cmpl_data
                    .append(cmpl_df)
                    .reset_index(drop=True))
 
    cmpl_md = metadata_dataset(cmpl_df, f, cmpl_out) 
    cmpl_metadata = (cmpl_metadata
                    .append(cmpl_md)
                    .reset_index(drop=True))

    inv_df = (df[df["Number:"].isnull()]
                .dropna(how='all', axis=0)
                .dropna(how='all',axis=1)
                .drop('Beat:', axis=1))
    inv_df.columns = ["CRID", "Full_Name", "Assignment", "Rank", "Star", "Appointed_Datetime"]
    inv_data = (inv_data
                    .append(inv_df)
                    .reset_index(drop=True))
 
    inv_md = metadata_dataset(inv_df, f, inv_out)
    inv_metadata = (inv_metadata
                    .append(inv_md)
                    .reset_index(drop=True))

cmpl_metadata.to_csv("../output/" +  "metadata_" + cmpl_out, index = False)
cmpl_data.to_csv("../output/" + cmpl_out , index = False)
inv_metadata.to_csv("../output/" +  "metadata_" + inv_out, index = False)
inv_data.to_csv("../output/" + inv_out , index = False)
