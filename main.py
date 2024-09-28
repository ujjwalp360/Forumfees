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
def load_data():
    df = pd.read_csv(CSV_FILE)
    st.write("Data loaded from CSV:")
    st.write(df)  # Print loaded data for debugging
    return df

# Append new data to the CSV
def append_data(roll_no, name, amount):
    df = load_data()
    
    # Check if the roll number already exists
    if roll_no in df['Roll No'].values:
        st.error(f"Roll No {roll_no} already exists. Please use a different roll number.")
        return

    new_data = pd.DataFrame({'Roll No': [roll_no], 'Name': [name], 'Amount': [amount]})
    
    # Append new data and save
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    st.success("Data submitted successfully!")
    st.write("Data After Appending:")
    st.write(df)

# Delete a row from the CSV
def delete_row(index):
    df = load_data()  # Load the current data
    if index < len(df):  # Check if the index is valid
        df = df.drop(index)  # Drop the selected row
        df.to_csv(CSV_FILE, index=False)  # Save the updated DataFrame back to CSV
        st.success("Row deleted successfully!")
    else:
        st.error("Invalid index for deletion.")

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

# Load data to show in the list when button is clicked
if st.button("Show List"):
    df = load_data()  # Load the data again when the button is pressed
    if not df.empty:
        df_sorted = df.sort_values(by='Roll No').reset_index(drop=True)  # Reset index for clean display
        st.write(df_sorted)
        
        # Calculate and display total amount
        total_amount = df['Amount'].sum()
        st.write(f"**Total Amount Collected:** ₹{total_amount}")

        # Option to delete a row
        delete_index = st.number_input("Enter the index of the row to delete", min_value=0, max_value=len(df)-1)
        if st.button("Delete Row"):
            delete_row(delete_index)
    else:
        st.write("No data available.")
