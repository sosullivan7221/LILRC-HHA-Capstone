## create a basic stremalit app
import streamlit as st
from scripts.convertcsv import convert_to_csv_file
from scripts.streamlit.westhampton_st import clean_westhampton
from scripts.streamlit.baldwin_st import clean_baldwin
from scripts.streamlit.airtable_st import clean_airtable
from scripts.streamlit.hampton_bays_st import clean_hampton_bays
from scripts.streamlit.lindenhurst_st import clean_lindenhurst
from scripts.streamlit.north_babylon_st import clean_north_babylon
from scripts.streamlit.smithtown_non_prof_st import clean_smithtown_non_prof
from scripts.streamlit.babylon_st import clean_bablyon
from scripts.streamlit.smithtown_prof_st import clean_smithtown_prof
import pandas as pd
from io import StringIO

## dictionary for cleaning functions

cleaning_functions = { 
    'westhampton' : clean_westhampton,
    'baldwin' : clean_baldwin,
    'airtable' : clean_airtable,
    'hampton bays' : clean_hampton_bays,
    'lindenhurst' : clean_lindenhurst,
    'north_babylon' : clean_north_babylon,
    'smithtown non-professional' : clean_smithtown_non_prof,
    'babylon' : clean_bablyon,
    'smithtown professional' : clean_smithtown_prof}

st.title('LILRC Salary Data Cleaning')

## create an file upload widget for .csv
uploaded_file = st.file_uploader("Upload Excel Data", type=['xlsx'])

## check if file is uploaded
if uploaded_file is not None:
    
    ## get the file name of the uploaded file
    file_name = uploaded_file.name

    ## get the file extension
    file_extension = file_name.split('.')[-1]

    ## print object type of uploaded file
    print('Object type: ', type(uploaded_file))

    try:
        if file_extension == 'xlsx':
           if file_name == 'Babylon.xlsx':
               df = pd.read_excel(uploaded_file, skiprows=4, usecols=[1,2,3,4])
           elif file_name == 'Smithtown Professional.xlsx':
               df = pd.read_excel(uploaded_file, skiprows=2)
           else:
               df = pd.read_excel(uploaded_file)
        else:
            print('Unknown file extension')
    except Exception as e:
        st.write(f'Error: {e}')
        
if df is not None:
    # Retrieve name of file
    base_name = file_name.split('.')[0].lower()
    
    # Get corresponding cleaning function
    cleaning_function = cleaning_functions.get(base_name)
    
    if cleaning_function:
        try:
            df_clean = cleaning_function(df)
            csv = df_clean.to_csv(index=False)
            st.download_button(label='Download cleaned data', data=csv, 
                           file_name='cleaned_data.csv', mime='text/csv')

        except Exception as e:
            st.write(f'Error: {e}')


        st.write(f'File name: {file_name}')
        st.write(f'File extension: {file_extension}')
        st.write('Cleaned data:')
        st.write(df_clean)
        
        st.write('------------')
    else:
        st.error('No cleaning function for this file')

# Run the app
# streamlit run app.py
