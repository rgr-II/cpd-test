import pandas as pd
import numpy as np
import os
import sys

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)

from helperfunctions import *
from utils import *
input_path = "../input/"
out_path = "../output/"
out_file = "accused.csv"

files = [input_path + f for f in os.listdir(input_path)]

data = pd.DataFrame()
metadata = pd.DataFrame()

for f in files:
    df = ReadMessy(f)
    df.insert(0, "CRID", (df["Number:"]
                            .fillna(method='ffill')
                            .astype(int)))
    df = (df.drop("Number:", axis=1)
            .dropna(thresh = len(df.columns.values)-1))
    df.columns = ["CRID", "Full_Name", "Birth_Year", "Gender", "Race", "Appointed_Date", "Current_Unit", "Current_Rank", "Star","Complaint_Category", "Recommended_Finding", "Recommended_Discipline", "Final_Finding", "Final_Discipline"]
    
    data = (data
            .append(df)
            .reset_index(drop=True))

    metadata = (metadata
                    .append(metadata_dataset(df, f, out_file)
                    .reset_index(drop=True)))

data.to_csv(out_path + out_file, index=False)
metadata.to_csv(out_path + "metadata_" +  out_file, index=False)
