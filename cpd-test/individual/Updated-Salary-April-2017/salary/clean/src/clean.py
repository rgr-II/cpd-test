import pandas as pd
import os

from CleaningFunctions import *

files = ['../input/' + f for f in os.listdir('../input/')]

for f in files[:1]:
    df = pd.read_csv(f)
    df = CleanData(df)
