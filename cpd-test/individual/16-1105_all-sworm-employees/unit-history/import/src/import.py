import pandas as pd
import os
from ImportFunctions import *

f = '../input/' + os.listdir('../input')[0]
df = pd.read_excel(f)
df.columns = ['Last_Name', 'First_Name', 'Gender', 'Race', 'Age', 'Appointed_Date', 'Unit', 'Effective_Date', 'End_Date'] + ['Star' + str(i) for i in range(1,11)]
df.to_csv('../output/unit-history.csv', index=False)
metadata_dataset(df, f, 'unit-history.csv').to_csv('../output/metadata_unit-history.csv',index=False)
