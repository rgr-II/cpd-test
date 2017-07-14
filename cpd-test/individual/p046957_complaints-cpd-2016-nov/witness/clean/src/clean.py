import os
import sys
import numpy as np
import pandas as pd

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)

from CleaningFunctions import *

input_path = "../input/"
out_path = "../output/"

df = pd.read_csv(input_path + "witnesses.csv")
df.loc[df['Race'] == 'WBH', 'Race'] = 'WWH'
CleanData(df, int_cols = ["Start", "Birth_Year"]).to_csv(out_path + 'witnesses.csv', index=False)
