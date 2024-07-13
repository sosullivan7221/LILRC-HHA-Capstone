import pandas as pd
import datetime
import os

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
        "Current Salary" : "Salary",
        "PT-FT" : "Part Time",
        "Institution" : "Library Name",
        }
    df.rename(columns=new_columns, inplace=True)

    # Convert 'Salary' from string to float, removing commas and dollar signs
    df['Salary'] = df['Salary'].astype(str).str.replace(',', '').str.replace('$','').str.replace('N/A','').astype(float)
    
    # Filter between salary and hourly based on value
    for index, row in df.iterrows():
        if row['Salary'] < 1000:
            df.at[index, 'Hourly'] = row['Salary']
            df.at[index, 'Salary'] = ''
        else:
            pass
    
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
    directory = 'data/raw/airtable/'
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):  # Make sure it's a CSV file
            file_path = os.path.join(directory, filename)
            clean_csv(file_path)

