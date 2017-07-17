import pandas as pd
import os
from CleaningFunctions import *
f = '../input/' + os.listdir('../input/')[0]
df = pd.read_csv(f)
df = CleanData(df, int_cols = ["Birth_Year"])
df.to_csv('../output/all-members.csv', index=False)
