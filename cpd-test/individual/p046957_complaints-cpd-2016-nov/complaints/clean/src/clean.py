import numpy as np
import pandas as pd

df = pd.read_csv("../../import/output/complaints.csv")
cmpl_df = df[~df["Number:"].isnull()]
inv_df = df[df["Number:"].isnull()]

print(cmpl_df.head(3))
print("********************")
print(inv_df.head(3))
'''
cmpl_df = df.loc[df["Number:"].isnull()]
inv_df = df[~df.isin(cmpl_df)].dropna()
print(cmpl_df.head(3))
print(inv_df.head(3))'''
