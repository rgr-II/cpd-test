import os
import sys
import numpy as np
import pandas as pd
from operator import itemgetter
import datetime
import itertools

module_path = os.path.abspath(os.path.join('../../../../../tools/'))
if module_path not in sys.path: sys.path.append(module_path)
from helperfunctions import *

input_path = "../input/"
out_path = "../output/"
outname = "complaints.csv"
files = [input_path + f for f in os.listdir(input_path)]

data = pd.DataFrame()

for f in files:
    df = ReadMessy(f)
    data = (data
            .append(df)
            .reset_index(drop=True))

cmpl_df = data[~data["Number:"].isnull()]
inv_df = data[data["Number:"].isnull()]

cmpl_df.to_csv("../output/" + "complaints.csv" , index = False)
inv_df.to_csv("../output/" + "investigators.csv" , index = False)
