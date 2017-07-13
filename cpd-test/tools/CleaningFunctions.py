import pandas as pd
import re

def IntColumn(x):
    if isinstance(x, str) and "." in x:
        return int(float(x))
    else:
        return int(x)

def CleanGender(g, gd = {'M':'MALE', 'F':'FEMALE', 'X':'UNKNOWN'}):
    if g in gd.values():
        return g
    else:
        return gd[g]

def CleanRace(r, rd = {'WHI':'WHITE', 'BLK':'BLACK', 'S':'WHITE', 'API':'API', 'I':'OTHER', 'U':'UNKNOWN', 'WWH':'HISPANIC', 'ASIAN/PACIFIC ISLANDER' : 'API', 'BLACK HISPANIC': 'BLACK', 'WHITE HISPANIC' : 'HISPANIC', 'AMER IND/ALASKAN NATIVE' : 'OTHER'}):
    if r in rd.values():
        return r
    else:
        return rd[r]

def ExtractSuffixName(x):
    suffixes = ('II', 'III', 'IV', 'JR', 'SR')
    suffix = [w for w in x.split(" ") if w in suffixes]
    return suffix[0] if suffix else ""

def ExtractMiddleInitital(x):
    xs = x.split(' ')
    if len(xs) > 1 and len(xs[0]) == 1:
        return xs[0]
    else:
        return ""

def StripName(x):
    x = re.sub(r'[^\w\s]', '', x)
    return ' '.join(x.split())

def CleanLastName(x):
    x = StripName(x)
    suffix = ExtractSuffixName(x)
    x = x.replace(suffix, "")

    return [''.join(x.split()), suffix]

def CleanFirstName(x):
    x = StripName(x)
    MI = ExtractMiddleInitital(x)
    return [''.join(x.replace(MI+" ", "").split()), MI]

def CleanDates(df):
    df_cols = df.columns.values
    dt_df = pd.DataFrame()
    for col in df_cols:
        col_suffix = col.split('_')[0]
        dt_df[col_suffix + "_Date"] = pd.to_datetime(df[col]).dt.date
        if 'time' in col:
            dt_df[col_suffix + '_Time'] = pd.to_datetime(df[col]).dt.time
    return dt_df

def CleanNames(df):
    df_cols = df.columns.values
    if 'Full_Name' in df_cols and 'Last_Name' not in df_cols: 
        name_df = pd.DataFrame(df['Full_Name']
                                .fillna(",")
                                .apply(lambda x: x.rsplit(',',1))
                                .values.tolist())
        LN = pd.DataFrame(name_df[0].apply(str.upper).apply(CleanLastName).values.tolist(), columns = ["Last_Name", "Suffix_Name"])
        FN = pd.DataFrame(name_df[1].apply(str.upper).apply(CleanFirstName).values.tolist(), columns = ["First_Name", "Middle_Initial"])
    else:
        LN = pd.DataFrame(df['Last_Name'].apply(str.upper).apply(CleanLastName).values.tolist(), columns = ['Last_Name', 'Suffix_Name'])
        FN = pd.DataFrame(df['First_Name'].apply(str.upper).apply(CleanFirstName).values.tolist(), columns = ['First_Name', 'Middle_Initital'])
    return  LN.join(FN)

def CleanData(df, skip_cols=[]):
    name_cols = ['Full_Name', "First_Name", "Last_Name", "Middle_Initital", "Suffix_Name"]
    df_cols = df.columns.values
    IntCols = ["Birth_Year", "Current_Unit", "Star", "Recommended_Discipline", "Final_Discipline"]
    if 'Gender' in df_cols and 'Gender' not in skip_cols:
        df['Gender'] = df['Gender'].apply(str.upper).apply(CleanGender)
    if 'Race' in df_cols and 'Race' not in skip_cols:
        df['Race'] = df['Race'].apply(str.upper).apply(CleanRace)
    for col in [IC for IC in df_cols if IC in IntCols and IC not in skip_cols]:
        df[col] = pd.to_numeric(df[col], errors = 'coerce', downcast = 'integer')
    if [col for col in df_cols if 'Date' in col]:
        dt_df = df[[DC for DC in df_cols if 'Date' in  DC]]
        df = df[list(set(df_cols) - set(dt_df.columns.values))].join(CleanDates(dt_df))
    if [col for col in df_cols if col in name_cols]:
        name_df = df[[col for col in df_cols if col in name_cols]]
        print(CleanNames(name_df))
        df = df[list(set(df_cols) - set(name_df.columns.values))].join(CleanNames(name_df))
    return df
