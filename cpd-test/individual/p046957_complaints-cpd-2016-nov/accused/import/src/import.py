import pandas as pd
import numpy as np
import os
import sys

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)

from helperfunctions import *

input_path = "../input/"
out_path = "../output/"

files = [input_path + f for f in os.listdir(input_path)]
data = pd.DataFrame()

for f in files:
    df = ReadMessy(f)
    df['Number:'] = (df['Number:']
                    .fillna(method='ffill')
                    .astype(int))
    df.dropna(thresh = len(df.columns.values)-1, inplace=True)

    data = (data
            .append(df)
            .reset_index(drop=True))

data.to_csv("../output/accused.csv", index=False)
