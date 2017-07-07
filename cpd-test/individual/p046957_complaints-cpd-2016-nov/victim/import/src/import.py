import pandas as pd
import numpy as np
import os
import sys

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)

from helperfunctions import *

input_path = '../input/'
f = input_path + os.listdir(input_path)[0]
df = ReadMessy(f)
df.insert(0, "CRID", (df['Number']
                        .fillna(method='ffill')
                        .astype(int)))
df = (df
        .dropna(thresh = len(df.columns.values)-1, axis = 0)
        .drop('Number', axis=1)
        .reset_index(drop = True))
df.columns = ['CRID', 'Gender', 'Age', 'Race'] 
df.to_csv("../output/victim.csv")
