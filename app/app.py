

# import necessary libraries
import streamlit as st
import pandas as pd

# Load the departures CSV file from datasets/air_traffic/departures.csv
departures_df = pd.read_csv("datasets/air_traffic/departures.csv")

# Display a table of first 20 rows of departures_df 
st.table(departures_df.head(20))

# Group the departures_df by month and count the frequencies.
month_count_df = departures_df.groupby('Month').count()

# Define title for Streamlit app
st.title("Air Traffic Report")

# Display a line chart of the frequencies of departures per month
st.line_chart(month_count_df)

