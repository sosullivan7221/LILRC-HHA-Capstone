import pandas as pd 
from data.mappingFile import mapping

### Data model to try:
        # - Column 1: Library Name (string)
        # - Column 2: Employee Number (int)
        # - Column 2: Job Title (string)
        # - Column 3: Part time/Full time (string)
        # - Column 4: Salary (int)
        # - Column 5: Year (int)

df_transformed_column_names = [
    'Library Name', 
    'Employee Number', 
    'Job Title', 
    'Part time/Full time', 
    'Salary', 
    'Year']


df = pd.read_csv('data/raw/Copy of Amagansett - Salary Data.csv')

# Standardizing column names
new_columns = {
    "Title": "Library Name",
    "Starting Annual Salary": "Salary",
    "Part time": "Part time/Full time"
}

df.rename(columns=new_columns, inplace=True)

# Convert 'Salary' from string to int, removing commas
df['Salary'] = df['Salary'].str.replace(',', '').astype(float)

# Fill in missing values for 'Part time/Full time' based on 'Starting Hourly Rate'
df['Part time/Full time'] = df['Starting Hourly Rate'].apply(lambda x: 'Part time' if pd.notna(x) else 'Full time')

# Determine 'Employee Number' and 'Year'
df['Employee Number'] = range(1, len(df) + 1)
df['Year'] = 2024  # Assuming all data is from the year 2024

# Selecting and reordering columns to match the desired format
final_columns = ['Employee Number', 'Part time/Full time', 'Salary', 'Year']
df = df[final_columns]

df

df.to_csv('data/transformed/amagansett.csv', index=False)