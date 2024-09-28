import streamlit as st
import pandas as pd
import os

# Specify the path to your CSV file
CSV_FILE = 'Fees.csv'

# Function to ensure the CSV file exists
def ensure_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])
        df.to_csv(CSV_FILE, index=False)
        st.write("Created a new CSV file.")
    elif os.stat(CSV_FILE).st_size == 0:
        df = pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])
        df.to_csv(CSV_FILE, index=False)
        st.write("CSV file was empty and has been recreated.")

# Load data from the CSV file and treat 'Roll No' as string to prevent float conversion
def load_data():
    try:
        df = pd.read_csv(CSV_FILE, dtype={'Roll No': str})
        return df
    except pd.errors.EmptyDataError:
        st.write("No data available in CSV.")
        return pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])

# Append new data to the CSV file, ensure 'Roll No' is treated as string
def append_data(roll_no, name, amount):
    df = load_data()

    # Check if roll number exists
    if roll_no in df['Roll No'].values:
        st.error(f"Roll No {roll_no} already exists. Please use a different roll number.")
        return

    # Append new data, explicitly cast 'Roll No' to string
    new_data = pd.DataFrame({'Roll No': [str(roll_no)], 'Name': [name], 'Amount': [amount]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    st.success("Data submitted successfully!")

# Streamlit app for collecting student data
st.title("Forum Fees Collection")

# Ensure the CSV exists before anything
ensure_csv()

# Form to input new student data
with st.form("entry_form"):
    name = st.text_input("Enter Name")
    roll_no = st.text_input("Enter Roll No (mandatory)", max_chars=4)  # Ensure Roll No is a string
    amount = st.number_input("Enter Amount", value=250)

    submit = st.form_submit_button("Submit")

    if submit:
        if roll_no.strip() == "":
            st.error("Roll No is mandatory. Please enter a valid Roll No.")
        else:
            append_data(roll_no.strip(), name, amount)

# Show the list of data
if st.button("Show List"):
    df = load_data()
    
    if not df.empty:
        df_sorted = df.sort_values(by='Roll No').reset_index(drop=True)
        df_sorted.index += 1  # Start index from 1
        
        # Ensure 'Roll No' is displayed as a string and strip any .0 (by casting to int if needed)
        df_sorted['Roll No'] = df_sorted['Roll No'].astype(str).str.replace(r'\.0$', '', regex=True)
        
        st.write(df_sorted)
        
        # Calculate total amount
        total_amount = df['Amount'].sum()
        st.write(f"**Amount Collected:** ₹{total_amount}")
        st.write(f"**Amount left:** ₹{13000 - total_amount}")
        st.write(f"**Total Amount to collect:** ₹13000")
        st.write(f"**No. of students left:** {(13000 - total_amount) // 250}")
    else:
        st.write("No data available.")
def delete_row_by_roll_no(roll_no):
    df = load_data()

    # Ensure roll number is treated as a string
    df['Roll No'] = df['Roll No'].astype(str)

    # Check if the roll number exists
    if roll_no in df['Roll No'].values:
        df = df[df['Roll No'] != roll_no]
        df.to_csv(CSV_FILE, index=False)  # Save the updated DataFrame back to CSV
        st.success(f"Roll No {roll_no} deleted successfully!")
    else:
        st.error(f"Roll No {roll_no} not found.")

with st.form("delete_form"):
    delete_roll_no = st.text_input("Enter the Roll No to delete")
    delete_submit = st.form_submit_button("Delete")

    if delete_submit:
        delete_row_by_roll_no(delete_roll_no)
