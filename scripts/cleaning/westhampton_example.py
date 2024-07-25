import pandas as pd
import datetime
import os
import re

def clean_df(df):
    
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
    # df = pd.read_csv(file)

    # Standardizing column names
    new_columns = {
        "annual_salary" : "Salary",
        "other_title" : "Job Title"
        }
    df.rename(columns=new_columns, inplace=True)
    
    # Drop filler columns
    df = df[['Job Title', 'Salary']]
    df.dropna(subset= ['Salary', 'Job Title'], inplace=True)
    
    # Convert 'Salary' from string to float, removing commas and dollar signs
    df['Salary'] = df['Salary'].astype(str).str.replace(',', '').str.replace('$','').str.replace(' ', '').astype(float)
    
    # Filter between salary and hourly based on value
    for index, row in df.iterrows():
        if row['Salary'] < 1000:
            df.at[index, 'Hourly'] = row['Salary']
            df.at[index, 'Salary'] = ''
        else:
            pass
    
    # Fill in missing values for 'Part time/Full time' based on 'Starting Hourly Rate'
    df['Part Time'] = df['Hourly'].apply(lambda x: 'Y' if pd.notna(x) else 'N')
    
    # Determine 'Employee Number' and 'Year'
    df['Employee Number'] = range(1, len(df) + 1)
    today = datetime.date.today()
    df['Year'] = today.year
        
    # Fill null values for job title with above value
    
    df['Job Title'] = df['Job Title'].fillna(method='ffill')
    
    # Add Library Name from file name
    library_name = 'Westhampton'
    df.insert(0,'Library Name', library_name)
    
    # Selecting and reordering columns to match the desired format
    final_columns = ['Year', 'Library Name', 'Employee Number', 'Job Title', 'Part Time', 'Salary', 'Hourly',]
    df = df[final_columns]
    
    # Filter out empty rows
    df = df[df[['Hourly', 'Salary']].notna().any(axis=1)]
    
    return df