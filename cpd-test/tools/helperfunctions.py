import pandas as pd
import numpy as np
import datetime
def ReadMessy(path, add_skip=1):
    # add roll column (number)
    # format column names ahead of time
    # detect meta data in columns
    df = pd.read_excel(path, rows=20)
    col_list = df.columns.tolist()
    # if [col if '\n' in col or len(col) > 40 for col in col_list]:
    #   metadata = True
    Report_Produced_Date = [x for x in col_list if isinstance(x, datetime.datetime)]
    col_list = [x for x in col_list if x not in Report_Produced_Date]
    FOIA_Request = [x for x in col_list if 'FOIA' in x][0]

    skip = np.where(df.iloc[:,0].str.contains('Number', na=False))[0][0]+add_skip
    df = (pd.read_excel(path, skiprows=skip)
            .dropna(how='all', axis=0)
            .dropna(how='all', axis=1))

    return df
