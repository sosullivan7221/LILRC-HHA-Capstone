## create a basic stremalit app
import streamlit as st
from scripts.convertcsv import convert_to_csv_file
from scripts.cleaning.westhampton_example import clean_df
import pandas as pd
from io import StringIO

st.title('My first app')

## create an file upload widget for .csv
uploaded_file = st.file_uploader("Upload Westhampon data", type=['xlsx'])

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
            df = convert_to_csv_file(uploaded_file)
        else:
            print('Unknown file extension')
    except Exception as e:
        st.write(f'Error: {e}')

    
    try:
        df_clean = clean_df(df) ## then clean the data
        csv = df_clean.to_csv(index=False)         ## save to csv in io memory
        st.download_button(label='Download cleaned data', data=csv, 
                           file_name='cleaned_data.csv', mime='text/csv')

    except Exception as e:
        st.write(f'Error: {e}')


    st.write(f'File name: {file_name}')
    st.write(f'File extension: {file_extension}')
    st.write('Cleaned data:')
    st.write(df_clean)
        
    st.write('------------')

## add in button to download cleaned data
st.write('Download cleaned data')



# Run the app
# streamlit run app.py
