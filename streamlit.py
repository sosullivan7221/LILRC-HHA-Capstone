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
from scripts.streamlit.formatted_st import clean_formatted
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
    'smithtown professional' : clean_smithtown_prof,
    'amagansett' : clean_formatted,
    'bellmore' : clean_formatted,
    'bethpage' : clean_formatted,
    'bridgehampton' : clean_formatted,
    'cold spring harbor' : clean_formatted,
    'copiague' : clean_formatted,
    'east islip' : clean_formatted,
    'emma clark library' : clean_formatted,
    'hauppauge' : clean_formatted,
    'island park' : clean_formatted,
    'mastics-moriches-shirley' : clean_formatted,
    'montauk' : clean_formatted,
    'north bellmore' : clean_formatted,
    'rockville center' : clean_formatted,
    'rosyln (bryant library)' : clean_formatted,
    'sea cliff' : clean_formatted,
    'seaford' : clean_formatted,
    'shelter island' : clean_formatted,
    'shelter rock' : clean_formatted,
    'south country' : clean_formatted,
    'unknown libraries' : clean_formatted}

st.title('LILRC Salary Data Cleaning')

## create an file upload widget for .csv
uploaded_files = st.file_uploader("Upload Excel Data", type=['xlsx'], accept_multiple_files= True)

dataframes = []

for file in uploaded_files:
    ## check if file is uploaded
    if file is not None:
        
        ## get the file name of the uploaded file
        file_name = file.name

        ## get the file extension
        file_extension = file_name.split('.')[-1]

        ## print object type of uploaded file
        print('Object type: ', type(file))

        try:
            if file_extension == 'xlsx':
                if file_name == 'Babylon.xlsx':
                    df = pd.read_excel(file, skiprows=4, usecols=[1,2,3,4], engine='openpyxl')
                elif file_name == 'Smithtown Professional.xlsx':
                    df = pd.read_excel(file, skiprows=2, engine='openpyxl')
                else:
                    df = pd.read_excel(file, engine='openpyxl')
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
                if cleaning_function == clean_formatted:
                    df_clean = cleaning_function(df)
                    df_clean['Library Name'] = base_name.capitalize()
                    csv = df_clean.to_csv(index=False, encoding='utf-8')
                    st.download_button(label='Download cleaned data', data=csv, 
                            file_name='cleaned_data.csv', mime='text/csv')
                else:    
                    df_clean = cleaning_function(df)
                    csv = df_clean.to_csv(index=False, encoding='utf-8')
                    st.download_button(label='Download cleaned data', data=csv, 
                            file_name='cleaned_data.csv', mime='text/csv')

            except Exception as e:
                st.write(f'Error: {e}')

        # Delete this stuff later !
        st.write(f'File name: {file_name}')
        st.write(f'File extension: {file_extension}')
        st.write('Cleaned data:')
        st.write(df_clean)
        
        st.write('------------')
        
        dataframes.append(df_clean)
    else:
        st.error('No cleaning function for this file')

if dataframes:        
    final_data = pd.concat(dataframes, ignore_index=True)
    st.write('Final Data')
    st.write(final_data)
else:
    st.write('No data')

# Run the app
# streamlit run app.py
