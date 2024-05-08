import pandas as pd 
import glob

## load all files across transformed folder and concatenate them into one dataframe

# Load all files in the transformed folder
files = glob.glob('data/transformed/*.csv')

# Load all files into a list
dfs = [pd.read_csv(file) for file in files]

# Concatenate all files into one dataframe
df = pd.concat(dfs, ignore_index=True)