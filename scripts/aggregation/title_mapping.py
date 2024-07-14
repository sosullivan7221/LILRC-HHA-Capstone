import csv
import pandas as pd
import os

mapping_file = 'data\clean\job_mapping.csv'

job_mapping = {}

with open(mapping_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        job_mapping[row['Titles (CIVIL SERVICE and non-civil service)']] = row['Standard Titles']
        

final = 'data\clean\clean.csv'
df = pd.read_csv(final)

df['Job Title'] = df['Job Title'].str.title()

df['Standard Titles'] = df['Job Title'].map(job_mapping)

directory = ''
output_csv_file = os.path.join(directory, 'data\clean\clean.csv')
df.to_csv(output_csv_file, index=False, encoding='utf-8')