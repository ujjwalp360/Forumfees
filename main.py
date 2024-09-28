import streamlit as st
import pandas as pd
import os

# File location
CSV_FILE = 'https://github.com/ujjwalp360/Forumfees/blob/b70f555f67484d699f6b84044599887244c02be4/Fees.csv'

# Load the data from CSV file
@st.cache_data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])

# Append new data to the CSV
def append_data(roll_no, name, amount):
    new_data = {'Roll No': roll_no, 'Name': name, 'Amount': amount}
    df = load_data()
    df = df.append(new_data, ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# Display the form
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
