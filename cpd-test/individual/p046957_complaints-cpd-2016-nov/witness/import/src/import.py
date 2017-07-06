import pandas as pd
import numpy as np
import os
import sys

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)

from helperfunctions import *
input_path = '../input/'

f = input_path + os.listdir(input_path)[0]

df = ReadMessy(f, add_skip=0)
# Add a way to automatically assign column names
df['CRID'] = (pd.to_numeric(df['Gender'], errors='coerce')
                .fillna(method='ffill')
                .astype(int))
print(df.columns)
df = (df[df['Gender'] != df['CRID'].astype(str)]
        .dropna(thresh = len(df.columns.values)-1)
        .reset_index(drop=True))
print(df.head(10))

