import streamlit as st
import pandas as pd

# Load and prepare data
@st.cache
def load_data():
    # Load the dataset from Excel (Update the path as needed)
    data = pd.read_excel(r'C:\Users\prajw\Documents\ResaluteAI.in\rawdata.xlsx')
    
    # Print columns and first few rows for debugging
    st.write("Available columns:", data.columns)
    st.write("First few rows of the data:", data.head())
    
    # Ensure 'date' column is in datetime format
    if 'date' not in data.columns:
        st.error("The 'date' column is not found in the dataset.")
        st.stop()
    
    # Check if 'location' column should be renamed if there are two
    if 'location' in data.columns and 'location.1' in data.columns:
        data.rename(columns={'location': 'location_1', 'location.1': 'location_2'}, inplace=True)
    
    data['date'] = pd.to_datetime(data['date'])
    return data

data = load_data()

# Compute datewise total duration for each inside and outside
if 'location_1' in data.columns:
    datewise_duration = data.groupby(['date', 'location_1'])['number'].sum().unstack().fillna(0)
else:
    datewise_duration = data.groupby(['date', 'location'])['number'].sum().unstack().fillna(0)

# Compute datewise number of picking and placing activities
datewise_activity = data.groupby(['date', 'activity']).size().unstack().fillna(0)

# Streamlit app
st.title('Data Analysis Dashboard')

st.header('1. Datewise Total Duration for Each Inside and Outside')
st.line_chart(datewise_duration)

st.header('2. Datewise Number of Picking and Placing Activity Done')
st.line_chart(datewise_activity)

# Optionally, display raw data
if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(data)
