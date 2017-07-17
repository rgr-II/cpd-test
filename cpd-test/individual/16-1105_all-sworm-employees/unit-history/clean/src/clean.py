import pandas as pd
import os
from CleaningFunctions import *
f = '../input/' + os.listdir('../input/')[0]
df = pd.read_csv(f)
df = CleanData(df, int_cols = ["Age","Unit"] + ['Star' + str(i) for i in range(1,11)])
df.to_csv('../output/unit-history.csv', index=False)
