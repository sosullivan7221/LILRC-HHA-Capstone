import pandas as pd
import datetime
import os

def clean_lindenhurst(df):
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
    df = pd.read_csv(df)

    # Standardizing column names
    new_columns = {
        "annual_salary" : "Salary",
        "part_time" : "Hourly",
        "civil_service_title" : "Job Title",
        }
    df.rename(columns=new_columns, inplace=True)

    # Convert 'Salary' from string to float, removing commas and dollar signs
    df['Salary'] = df['Salary'].astype(str).str.replace(',', '').str.replace('$','').str.replace('nan','').str.replace('n/a','').str.replace(' ','')

    # Convert 'Hourly' from string to float, removing commas and dollar signs
    df['Hourly'] = df['Hourly'].astype(str).str.replace(',', '').str.replace('$','').str.replace('nan','').str.replace('n/a','').str.replace(' ','')
    
    # Fill in missing values for 'Part time/Full time' based on 'Starting Hourly Rate'
    df['Part Time'] = df['Salary'].apply(lambda x: 'N' if pd.notna(x) else 'Y')
    
    # Determine 'Employee Number' and 'Year'
    df['Employee Number'] = range(1, len(df) + 1)
    today = datetime.date.today()
    df['Year'] = today.year
    
    # Fill null values for job title with above value
    df['Job Title'] = df['Job Title'].fillna(method='ffill')
    
    # Add Library Name from file name
    library_name = 'Lindenhurst'
    df.insert(0,'Library Name', library_name)
    
    # Selecting and reordering columns to match the desired format
    final_columns = ['Year', 'Library Name', 'Employee Number', 'Job Title', 'Part Time', 'Salary', 'Hourly',]
    df = df[final_columns]
    
    # Filter out empty rows
    df = df[df[['Hourly', 'Salary']].notna().any(axis=1)]
    
    return df