import pandas as pd
import datetime
import os

def clean_formatted(df):
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
        "annual_salary" : "Salary",
        "Annual Salary" : "Salary",
        " Annual Salary 6-7-24" : "Salary",
        "Hourly Rate-6-7-24" : "Hourly",
        "Hourly Rate" : "Hourly",
        "Hourly Rate " : "Hourly",
        "hour_rate" : "Hourly",
        "Hourly Rate (Part-Time)" : "Hourly",
        "part_time" : "Part Time",
        "Part-Time" : "Part Time",
        "Part time" : "Part Time",
        "Full/Part Time" : "Part Time",
        "civil_service_title" : "Title (civil servce title for civil service libraries)",
        "other_title" : "Other Title (if different than civil service title)",
        "Other Title (if different than civil service)" : "Other Title (if different than civil service title)"
        }
    df.rename(columns=new_columns, inplace=True)

    # Convert 'Salary' from string to float, removing commas and dollar signs
    df['Salary'] = df['Salary'].astype(str).str.replace(',', '').str.replace('$','').str.replace('N/A','')

    # Convert 'Hourly' from string to float, removing commas and dollar signs
    df['Hourly'] = df['Hourly'].astype(str).str.replace(',', '').str.replace('$','').str.replace('N/A','')
    
    # Convert ranges into averages
    
    def average_from_range(value):
        if pd.isna(value) or not value:
            return None  # Return None if the value is NaN or empty
        value_str = str(value)
        try:
            if ' to ' in value_str:
                start, end = map(float, value_str.split(' to '))
                return (start + end) / 2
            elif '-' in value_str:
                start, end = map(float, value_str.split('-'))
                return (start + end) / 2
            elif ' - ' in value_str:
                start, end = map(float, value_str.split(' - '))
                return (start + end) / 2
            else:
                return float(value_str)
        except ValueError:
            return None

    # Apply the function to non-empty values only
    df['Salary'] = df['Salary'].apply(lambda x: average_from_range(x) if pd.notna(x) and x != '' else None)
    df['Hourly'] = df['Hourly'].apply(lambda x: average_from_range(x) if pd.notna(x) and x != '' else None)
    
    # Remove N/A from empty titles
    
    df['Other Title (if different than civil service title)'] = df['Other Title (if different than civil service title)'].astype(str).str.replace('N/A', '')

    # Fill in values for 'Part time/Full time'
    def convert_PT(value):
        if pd.isna(value):
            return 'N'
        elif value in ['No,', 'no', 'NO' 'FALSE', 'False', 'false', 'Full Time', 'F/T', 'FT']:
            return 'N'
        elif value in ['Yes', 'yes', 'YES', 'TRUE', 'True', 'true', 'Part Time', 'P/T', 'PT', 'x', 'X']:
            return 'Y'
        else:
            return 'N'
    df['Part Time'] = df['Part Time'].astype(str).apply(convert_PT)

    # Determine 'Employee Number' and 'Year'
    df['Employee Number'] = range(1, len(df) + 1)
    today = datetime.date.today()
    df['Year'] = today.year  
    
    # Merge job titles into one column
    job_title = df['Title (civil servce title for civil service libraries)'].fillna(df['Other Title (if different than civil service title)'])
    df.insert(1,'Job Title', job_title)
    
    # Add Library Name from file name
    library_name = 'Placeholder'
    df.insert(0,'Library Name', library_name)
    
    # Selecting and reordering columns to match the desired format
    final_columns = ['Year', 'Library Name', 'Employee Number', 'Job Title', 'Part Time', 'Salary', 'Hourly',]
    df = df[final_columns]
    
    # Filter out empty rows
    df = df[df[['Hourly', 'Salary']].notna().any(axis=1)]
    
    return df
