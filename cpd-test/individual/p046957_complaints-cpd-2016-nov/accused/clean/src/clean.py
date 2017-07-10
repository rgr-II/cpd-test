import os
import sys
import numpy as np
import pandas as pd

input_path = "../input/"
out_path = "../output/"

df = pd.read_csv(input_path + "accused.csv")

def IntColumn(x):
    if isinstance(x, str) and "." in x:
        return int(float(x))
    else:
        return int(x)

gender_dict = {"male" : "Male", "female":"Female", "m":"Male", "f" : "Female"}
def CleanGender(g, gd = gender_dict):
    return gd[g.lower()]
    
