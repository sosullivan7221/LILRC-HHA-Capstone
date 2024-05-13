import pandas as pd 
import datetime

### Data model to try:
        # - Column 1: Library Name (string)
        # - Column 2: Employee Number (int)
        # - Column 2: Job Title (string)
        # - Column 3: Part time (stirng)
        # - Column 4: Salary (int)
        # - Column 5: Hourly (int)
        # - Column 6: Year (int)

df_transformed_column_names = [
    'Library Name', 
    'Employee Number', 
    'Job Title', 
    'Part time', 
    'Salary',
    'Hourly', 
    'Year']




df = pd.read_csv('data/raw/Copy of Baldwin - Salary Data.csv')

# Standardizing column names
new_columns = {
    "Starting Annual Salary": "Salary",
    "Starting Hourly Rate" : "Hourly"
}

df.rename(columns=new_columns, inplace=True)

df.dtypes

# Convert 'Salary' from string to int, removing commas
df['Salary'] = df['Salary'].astype(str).str.replace(',', '').astype(float)

# Convert 'Hourly' from string to int, removing commas
df['Hourly'] = df['Hourly'].astype(str).str.replace(',', '').astype(float)

# Fill in missing values for 'Part time/Full time' based on 'Starting Hourly Rate'
df['Part time'] = df['Part time'].str.replace('FULL TIME', 'No').str.replace('PART TIME', 'Yes')

# Determine 'Employee Number' and 'Year'
df['Employee Number'] = range(1, len(df) + 1)
today = datetime.date.today()
df['Year'] = today.year  

# Add Library Name as a column

df['Library Name'] = 'Baldwin'

# Selecting and reordering columns to match the desired format
final_columns = ['Year', 'Library Name','Employee Number', 'Part time', 'Salary', 'Hourly',]
df = df[final_columns]

df

df.to_csv('data/transformed/baldwin.csv', index=False)