import pandas as pd
import os

from ImportFunctions import *

files = ['../input/' + f for f in os.listdir('../input/')]

for f in files:
    xls = pd.ExcelFile(f)
    for s in xls.sheet_names:
        df = xls.parse(s)
        df.columns = ["Last_Name", "First_Name", "Middle_Initial", "Gender", "Age_at_Hire", "Title", "Start_Date", "SPP", "Org_Hire_Date", "Salary", "Pay_Grade", "Employee_Status"]
        df.to_csv("salary-" + s + ".csv", index=False)
        metadata_dataset(df ,f + "-" + s, "salary-"+s+".csv").to_csv('metadata_' + 'salary-' + s + '.csv', index=False)
