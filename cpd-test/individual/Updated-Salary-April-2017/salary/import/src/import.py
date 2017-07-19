import pandas as pd
import os

from ImportFunctions import *

files = ['../input/' + f for f in os.listdir('../input/')]

for f in files:
    xls = pd.ExcelFile(f)
    for s in xls.sheet_names:
        df = xls.parse(s)
        df.columns = CorrectColumns(df.columns)
        df.to_csv("../output/salary-" + s + ".csv", index=False)
        metadata_dataset(df ,f + "-" + s, "salary-"+s+".csv").to_csv('../output/metadata_' + 'salary-' + s + '.csv', index=False)
