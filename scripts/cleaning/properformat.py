import pandas as pd
import datetime
import os

def clean_csv(file_path):
    # Data model
    df_transformed_column_names = [
        'Library Name', 
        'Employee Number', 
        'Job Title', 
        'Part time', 
        'Salary',
        'Hourly', 
        'Year'
    ]
    
    # Read CSV file
    df = pd.read_csv(file_path)

    # Standardizing column names
    new_columns = {
        "Starting Annual Salary": "Salary",
        "Starting Hourly Rate" : "Hourly"
    }
    df.rename(columns=new_columns, inplace=True)

    # Convert 'Salary' from string to float, removing commas and dollar signs
    df['Salary'] = df['Salary'].astype(str).str.replace(',', '').str.replace('$','').astype(float)

    # Convert 'Hourly' from string to float, removing commas and dollar signs
    df['Hourly'] = df['Hourly'].astype(str).str.replace(',', '').str.replace('$','').astype(float)

    # Fill in values for 'Part time/Full time'
    df['Part time'] = df['Part time'].apply(lambda x: 'Yes' if pd.notna(x) else 'No')

    # Determine 'Employee Number' and 'Year'
    df['Employee Number'] = range(1, len(df) + 1)
    today = datetime.date.today()
    df['Year'] = today.year  

    # Selecting and reordering columns to match the desired format
    final_columns = ['Year', 'Employee Number', 'Part time', 'Salary', 'Hourly',]
    df = df[final_columns]

    # Save the transformed data to CSV
    output_file_path = os.path.join('data/transformed', os.path.basename(file_path))
    df.to_csv(output_file_path, index=False)
    print(f"Cleaned file saved to: {output_file_path}")

if __name__ == "__main__":
    directory = 'data/raw/formatted/'
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):  # Make sure it's a CSV file
            file_path = os.path.join(directory, filename)
            clean_csv(file_path)

