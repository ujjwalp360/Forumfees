import streamlit as st
import pandas as pd
import os

# Get the current working directory
CURRENT_DIR = os.getcwd()
CSV_FILE = os.path.join(CURRENT_DIR, 'Fees.csv')

# Load the data from the CSV file
@st.cache_data
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df
    else:
        return pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])

# Append new data to the CSV using pd.concat()
def append_data(roll_no, name, amount):
    new_data = pd.DataFrame({'Roll No': [roll_no], 'Name': [name], 'Amount': [amount]})
    df = load_data()
    
    # Use pd.concat to add the new row
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save updated dataframe to CSV
    df.to_csv(CSV_FILE, index=False)

# Streamlit app for collecting student data
st.title("College Fee Collection")

with st.form("entry_form"):
    name = st.text_input("Enter Name")
    roll_no = st.text_input("Enter Roll No")
    amount = st.number_input("Enter Amount", value=250)
    
    # Form submit button
    submit = st.form_submit_button("Submit")

    if submit:
        append_data(roll_no, name, amount)
        st.success("Data submitted successfully!")

# Option to view the list sorted by roll number
if st.button("Show List"):
    df = load_data()
    if not df.empty:
        df_sorted = df.sort_values(by='Roll No')
        st.write(df_sorted)
        
        # Calculate and display total amount
        total_amount = df['Amount'].sum()
        st.write(f"**Total Amount Collected:** ₹{total_amount}")
    else:
        st.write("No data available.")
