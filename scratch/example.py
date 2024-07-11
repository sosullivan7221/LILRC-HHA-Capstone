import pandas as pd 
import numpy as np

## babylon 

# babylon = pd.read_excel(
#     'scratch/Babylon.xlsx',
#     sheet_name='Salary Survey 2024',
#     skiprows=4,
#     usecols='B:E'
#     )

# babylon.columns


babylon = pd.read_excel(
    'scratch/Babylon.xlsx',
    sheet_name='Salary Survey 2024',
    )

## conver NaN to missing
babylon = babylon.fillna(np.nan)

## get row count
babylon.shape[0]

## get a count of missing by column
babylon.isnull().sum()

## if a column has 100% missing, drop it
babylon = babylon.dropna(axis=1, how='all')

## loop through rows and detect where first non-missing row is, and make that the header
header = 0
for i in range(babylon.shape[0]):
    if babylon.iloc[i].notnull().sum() > 0:
        header = i
        break

babylon.columns = babylon.iloc[header]

## drop the rows that were used as the header
babylon = babylon.drop(range(header+1))

babylon.to_csv('scratch/babylon_clean.csv', index=False)




def excel_loader(yournameforit, filelocation, sheet):

    ##### load Bayshore-Brightwater.xlsx
    df = pd.read_excel(
        filelocation,
        sheet_name=sheet,
        )

    ## conver NaN to missing
    df = df.fillna(np.nan)

    ## if column names contain or start with 'Unamed: ' do the following
    if df.columns.str.contains('Unnamed:').sum() > 0:

        ## determine how many rows to skip
        skiprows = 0
        for i in range(df.shape[0]):
            if df.iloc[i].str.contains('Unnamed:').sum() > 0:
                skiprows = i
                break

        ## convert first three rows to all strings
        df.iloc[:skiprows] = df.iloc[:skiprows].astype(str)

        ## for the first three rows, replace 'NaN' with ''
        df.iloc[:skiprows] = df.iloc[:skiprows].replace('nan', '')

        ## merge the rows into a single row
        df.columns = df.iloc[:skiprows].apply(lambda x: ' '.join(x), axis=0)

        ## then drop the rows that were merged
        df = df.drop(range(skiprows))

        ## drop columns with all missing values
        df = df.dropna(axis=1, how='all')

        df.to_csv(f'scratch/{yournameforit}.csv', index=False)

    else:
        print('No cleaning needed')
        df.to_csv(f'scratch/{yournameforit}.csv', index=False)

    return 'Done!'


excel_loader('testdef_bayshore', 'scratch/Bayshore-Brightwater.xlsx', 'Sheet1')
excel_loader('testdef_babylon', 'scratch/Babylon.xlsx', 'Salary Survey 2024')