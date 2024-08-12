## create a basic stremalit app
import streamlit as st
from westhampton_st import clean_westhampton
from baldwin_st import clean_baldwin
from airtable_st import clean_airtable
from hampton_bays_st import clean_hampton_bays
from lindenhurst_st import clean_lindenhurst
from north_babylon_st import clean_north_babylon
from smithtown_non_prof_st import clean_smithtown_non_prof
from babylon_st import clean_bablyon
from smithtown_prof_st import clean_smithtown_prof
from formatted_st import clean_formatted
from no_box_st import clean_no_box
from no_lib_st import clean_no_lib
import pandas as pd

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
    'unknown libraries' : clean_formatted,
    'connetquot' : clean_no_box,
    'deer park' : clean_no_box,
    'freeport' : clean_no_box,
    'longwood' : clean_no_box,
    'lynnbrook' : clean_no_box,
    'middle country' : clean_no_box,
    'oyster bay-east norwich' : clean_no_box,
    'peninsula public library' : clean_no_box,
    'port washington' : clean_no_box,
    'riverhead' : clean_no_box,
    'sachem' : clean_no_box,
    'southampton (rogers memorial)' : clean_no_box,
    'wantagh' : clean_no_box,
    'west babylon' : clean_no_box}

st.title('LILRC Salary Data Cleaning')

## create an file upload widget for .csv
uploaded_files = st.file_uploader("Upload Excel Data", type=['xlsx'], accept_multiple_files= True)
mapping_file = st.file_uploader("Upload Title Mapping", type=['xlsx'])

## empty list for aggregation
dataframes = []

for file in uploaded_files:
    ## check if file is uploaded
    if file is not None:
        
        ## get the file name of the uploaded file
        file_name = file.name
        st.write(file_name)

        ## get the file extension
        file_extension = file_name.split('.')[-1]
        st.write(file_extension)

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
        cleaning_function = cleaning_functions.get(base_name, clean_no_lib)
        
        if cleaning_function:
            try:
                if cleaning_function == clean_formatted or cleaning_function == clean_no_box:
                    df_clean = cleaning_function(df)
                    df_clean['Library Name'] = base_name.capitalize()
                    csv = df_clean.to_csv(index=False, encoding='utf-8')

                elif cleaning_function == clean_no_lib:
                    df_clean = cleaning_function(df)
                    df_clean['Library Name'] = base_name.capitalize()
                    csv = df_clean.to_csv(index=False, encoding='utf-8')
                    
                    st.write(f'No cleaning file in record for {base_name} . Attempted clean with default script.')
                    st.write(f'File name: {file_name}')
                    st.write('Cleaned data:')
                    st.write(df_clean)
                else:    
                    df_clean = cleaning_function(df)
                    csv = df_clean.to_csv(index=False, encoding='utf-8')

            except Exception as e:
                st.write(f'Error: {e}')
                
        dataframes.append(df_clean)
    else:
        st.error('No cleaning function for this file')

if dataframes and mapping_file is not None:        
    final_data = pd.concat(dataframes, ignore_index=True)
    
    df_mapping = pd.read_excel(mapping_file)
    mapping_dictionary = dict(zip(df_mapping['survey_response_title'].str.title(), df_mapping['standardized_title']))
    
    final_data['Job Title'] = final_data['Job Title'].str.title()

    standard_titles = final_data['Job Title'].map(mapping_dictionary)
    final_data.insert(4, 'Standard Titles', standard_titles)
    
    
    st.write('Final Data')
    st.write(final_data)
    st.download_button(label='Download cleaned data', data=csv, 
                    file_name='cleaned_data.csv', mime='text/csv')
else:
    st.write('No data')

# Run the app
# streamlit run app.py
