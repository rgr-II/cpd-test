import pandas as pd
import os
from ImportFunctions import *
f = os.listdir('../input/')[0]
df = pd.read_excel('../input/'+f)
df.columns = ['Last_Name', 'First_Name', 'Middle_Initial', 'Gender', 'Race', 'Birth_Year', 'Appointed_Date', 'Current_Rank', 'Seniority_Date']
df[df['Last_Name'].str.len() <= 20].to_csv('../output/all-members.csv', index=False)
notes = df[df['Last_Name'].str.len() > 20]['Last_Name'].rename('Notes')
metadata_dataset(df[df['Last_Name'].str.len() <= 20], f, 'all-members.csv', notes = notes).to_csv('../output/metadata_all-members.csv', index=False)
