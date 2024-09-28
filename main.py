import streamlit as st
import pandas as pd
import os

# Specify the path to your CSV file
CSV_FILE = 'Fees.csv'  # Ensure this file is in the same directory as your Streamlit app

# Function to ensure the CSV file exists and is properly formatted
def ensure_csv():
    if not os.path.exists(CSV_FILE):
        # Create a new CSV file with the correct columns
        df = pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])
        df.to_csv(CSV_FILE, index=False)
        st.write("Created a new CSV file.")
    elif os.stat(CSV_FILE).st_size == 0:
        # Recreate if the file is empty
        df = pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])
        df.to_csv(CSV_FILE, index=False)
        st.write("CSV file was empty and has been recreated.")

# Load data from the CSV file
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv(CSV_FILE)
    st.write("Data loaded from CSV:")
    st.write(df)  # Print loaded data for debugging
    return df

# Append new data to the CSV
def append_data(roll_no, name, amount):
    new_data = pd.DataFrame({'Roll No': [roll_no], 'Name': [name], 'Amount': [amount]})
    
    # Load existing data
    df = load_data()
    
    # Print before appending for debugging
    st.write("Existing Data Before Appending:")
    st.write(df)

    # Append new data and save
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    # Print after appending for debugging
    st.write("Data After Appending:")
    st.write(df)

# Streamlit app for collecting student data
st.title("College Fee Collection")

ensure_csv()  # Ensure the CSV file is ready

with st.form("entry_form"):
    name = st.text_input("Enter Name")
    roll_no = st.text_input("Enter Roll No")
    amount = st.number_input("Enter Amount", value=250)

    submit = st.form_submit_button("Submit")

    if submit:
        append_data(roll_no, name, amount)
        st.success("Data submitted successfully!")

# Load data to show in the list
df = load_data()

if st.button("Show List"):
    if not df.empty:
        df_sorted = df.sort_values(by='Roll No')
        st.write(df_sorted)
        
        # Calculate and display total amount
        total_amount = df['Amount'].sum()
        st.write(f"**Total Amount Collected:** ₹{total_amount}")
    else:
        st.write("No data available.")
