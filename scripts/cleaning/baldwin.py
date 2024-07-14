import pandas as pd
import datetime
import os
import numpy as np

print('CWD', os.getcwd())
def clean_csv(file_path):
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
    df = pd.read_csv(file_path)

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
    
    def average_from_range(range_str):
        if ' to ' in range_str:
            start, end = map(float, range_str.split(' to '))
            return (start + end) / 2
        elif '-' in range_str:
            start, end = map(float, range_str.split('-'))
            return (start + end) / 2
        elif ' - ' in range_str:
            start, end = map(float, range_str.split(' - '))
            return (start + end) / 2
        else:
            return float(range_str)
    
    df['Salary'] = df['Salary'].apply(average_from_range)
    df['Hourly'] = df['Hourly'].apply(average_from_range)
    
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
    
    # Clean job titles
    df['Job Title'] = df['Job Title'].str.lstrip()
    
    mask = (df['Job Title'].str.len() > 1) & (df['Job Title'].str.len() < 4)
    df.loc[mask, 'Job Title'] = np.nan
    
    df['Job Title'] = df['Job Title'].fillna(method='ffill')
    
    # Add Library Name from file name
    library_name = os.path.splitext(os.path.basename(file_path))[0]
    df.insert(0,'Library Name', library_name)
    
    # Selecting and reordering columns to match the desired format
    final_columns = ['Year', 'Library Name', 'Employee Number', 'Job Title', 'Part Time', 'Salary', 'Hourly',]
    df = df[final_columns]
    
    # Filter out empty rows
    df = df[df[['Hourly', 'Salary']].notna().any(axis=1)]
    
     # Save the transformed data to CSV
    output_file_path = os.path.join('data/transformed', os.path.basename(file_path))
    df.to_csv(output_file_path, index=False)
    print(f"Cleaned file saved to: {output_file_path}")

if __name__ == "__main__":
    directory = 'data/raw/baldwin/'
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):  # Make sure it's a CSV file
            file_path = os.path.join(directory, filename)
            clean_csv(file_path)