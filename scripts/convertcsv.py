import pandas as pd
import os

def convert_to_csv(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):  # Check if it's an Excel file
            excel_file_path = os.path.join(directory, filename)
            # Load Excel file into a DataFrame
            df = pd.read_excel(excel_file_path)
            # Define the CSV output file path
            csv_output_path = os.path.splitext(excel_file_path)[0] + '.csv'
            # Save DataFrame to CSV
            df.to_csv(csv_output_path, index=False)
            print(f"Converted: {excel_file_path} to CSV: {csv_output_path}")

def convert_to_csv_file(uploaded_file):
    try:
        # Load Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        return f'Error: {e}'

if __name__ == "__main__":
    directory = 'data/raw/formatted/'
    convert_to_csv(directory)