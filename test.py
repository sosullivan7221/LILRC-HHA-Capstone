import pandas as pd

# Read CSV file
df = pd.read_csv('data/raw/babylon/Babylon.csv',
                    skiprows = 4,
                    usecols = [1,2,3,4])

print(df)
