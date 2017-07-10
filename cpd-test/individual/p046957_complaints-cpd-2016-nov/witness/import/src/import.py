import pandas as pd
import numpy as np
import os
import sys

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)

from helperfunctions import *
from utils import *

input_path = '../input/'
out_path = '../output/'
out_file = 'witnesses.csv'

f = input_path + os.listdir(input_path)[0]

df = ReadMessy(f, add_skip=0)
df.insert(0,"CRID",(pd.to_numeric(df['Gender'], errors='coerce')
                .fillna(method='ffill')
                .astype(int)))
df = (df[df['Gender']!=df['CRID'].astype(str)]
        .dropna(thresh=len(df.columns.values)-1)
        .reset_index(drop=True))
df.columns = ["CRID", "Full_Name", "Gender", "Race", "Star", "Birth_Year", "Appointed_Date"]

df.to_csv(out_path + out_file, index=False)
metadata_dataset(df, f, out_file).to_csv(out_path + "metadata_" + out_file, index=False)
