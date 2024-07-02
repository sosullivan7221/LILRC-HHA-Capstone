import pandas as pd
import datetime
import os
import re

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
        "Hourly Rate" : "Hourly",
        "Hourly Rate " : "Hourly",
        "hour_rate" : "Hourly",
        "Hourly Rate (Part-Time)" : "Hourly",
        "part_time" : "Part Time",
        "Part-Time" : "Part Time",
        "Full/Part Time" : "Part Time",
        "civil_service_title" : "Title (civil servce title for civil service libraries)",
        "other_title" : "Other Title (if different than civil service title)",
        "CS Title" : "Title (civil servce title for civil service libraries)"
        }
    df.rename(columns=new_columns, inplace=True)
    
    # Convert 'Salary' from string to float, removing commas and dollar signs
    df['Salary'] = df['Salary'].astype(str).str.replace(',', '').str.replace('$','').str.replace(' ', '').astype(float)
    
    #if df['Salary'].isnull == False:
        #df['Salary'] = df['Salary'].astype(str).apply(lambda x: re.sub(r'[^\d|\.]', '', x) if pd.notna(x) else None).astype(float)
    #else:
        #pass
    
    # Convert 'Hourly' from string to float, removing commas and dollar signs
    df['Hourly'] = df['Hourly'].astype(str).str.replace(',', '').str.replace('$','').str.replace(' ', '').str.replace('/hr', '').astype(float)
    
    #if df['Hourly'].isnull == False:
        #df['Hourly'] = df['Hourly'].astype(str).apply(lambda x: re.sub(r'[^\d|\.]', '', x) if pd.notna(x) else None).astype(float)
    #else:
        #pass
    
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
    
    # Merge job titles into one column
    if 'Other Title (if different than civil service title)' in df.columns:
        job_title = df['Title (civil servce title for civil service libraries)'].fillna(df['Other Title (if different than civil service title)'])
        df.insert(1,'Job Title', job_title)
    else:
        job_title = df['Title (civil servce title for civil service libraries)']
        df.insert(1,'Job Title', job_title)
        
    # Fill null values for job title with above value
    
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
    directory = 'data/raw/no_box/'
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):  # Make sure it's a CSV file
            file_path = os.path.join(directory, filename)
            clean_csv(file_path)
    