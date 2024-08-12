import pandas as pd
import datetime
import os
import re

def clean_smithtown_non_prof(df):
    # Data model
    df_transformed_column_names = [
        'Library Name', 
        'Employee Number', 
        'Job Title', 
        'Part Time', 
        'Salary',
        'Hourly', 
        'Year'
    ]
    
    # Read CSV file
    # df = pd.read_csv(file_path)

    # Standardizing column names
    new_columns = {
        "Mean" : "Salary",
        "TITLE" : "Job Title"
        }
    df.rename(columns=new_columns, inplace=True)
    
    # Remove Bi-Weekly and Hourly Rows 
    df = df[~df['Job Title'].isin(['BI-WKLY', 'HOURLY', 'TITLE'])]
    df.dropna(subset= ['Salary'], inplace=True)
    
    # Convert 'Salary' from string to float, removing commas and dollar signs
    df['Salary'] = df['Salary'].astype(str).str.replace(',', '').str.replace('$','').str.replace(' ', '').astype(float)
    
     # Duplicate Rows based on # of Employees Column
    df['# of Employees'] = df['# of Employees'].astype(str).str.replace('0', '1').astype(float)
    df = df.loc[df.index.repeat(df['# of Employees'])].reset_index(drop=True)
    
    # Filter between salary and hourly based on value
    for index, row in df.iterrows():
        if row['Salary'] < 1000:
            df.at[index, 'Hourly'] = row['Salary']
            df.at[index, 'Salary'] = ''
        else:
            pass
    
    # Fill in missing values for 'Part time/Full time' based on 'Starting Hourly Rate'
    df['Part Time'] = df['Salary'].apply(lambda x: 'N' if pd.notna(x) else 'Y')
    
    # Determine 'Employee Number' and 'Year'
    df['Employee Number'] = range(1, len(df) + 1)
    today = datetime.date.today()
    df['Year'] = today.year
        
    # Fill null values for job title with above value
    
    df['Job Title'] = df['Job Title'].fillna(method='ffill')
    
    # Add Library Name from file name
    library_name = 'Smithtown Non-Professional'
    df.insert(0,'Library Name', library_name)
    
    # Selecting and reordering columns to match the desired format
    final_columns = ['Year', 'Library Name', 'Employee Number', 'Job Title', 'Part Time', 'Salary']
    df = df[final_columns]
    
    # Filter out empty rows
    df = df[df[['Salary']].notna().any(axis=1)]
    
    return df