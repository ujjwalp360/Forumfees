import streamlit as st
import pandas as pd
import os

# Specify the path to your CSV file
CSV_FILE = 'Fees.csv'  # Ensure this file is in the same directory as your Streamlit app

# Function to ensure the CSV file exists and is properly formatted
def ensure_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])
        df.to_csv(CSV_FILE, index=False)
        st.write("Created a new CSV file.")
    elif os.stat(CSV_FILE).st_size == 0:
        df = pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])
        df.to_csv(CSV_FILE, index=False)
        st.write("CSV file was empty and has been recreated.")

# Load data from the CSV file
def load_data():
    if os.stat(CSV_FILE).st_size == 0:
        return pd.DataFrame(columns=['Roll No', 'Name', 'Amount'])
    return pd.read_csv(CSV_FILE, dtype={'Roll No': str})  # Ensure 'Roll No' is treated as string

# Append new data to the CSV
def append_data(roll_no, name, amount):
    df = load_data()

    # Check if the roll number already exists
    if roll_no in df['Roll No'].astype(str).values:
        st.error(f"Roll No {roll_no} already exists. Please use a different roll number.")
        return

    # Append new data
    new_data = pd.DataFrame({'Roll No': [str(roll_no)], 'Name': [name], 'Amount': [amount]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    st.success("Data submitted successfully!")

# Delete a row by roll number from the CSV
def delete_row_by_roll_no(roll_no):
    df = load_data()
    roll_no = roll_no.strip()  # Trim any leading/trailing spaces

    # Ensure roll number is treated as a string
    df['Roll No'] = df['Roll No'].astype(str)

    # Check if the roll number exists
    if roll_no in df['Roll No'].values:
        df = df[df['Roll No'] != roll_no]  # Remove the row with the given roll number
        df.to_csv(CSV_FILE, index=False)  # Save the updated DataFrame back to CSV
        st.success(f"Roll No {roll_no} deleted successfully!")

        # Display the updated list automatically after deletion
        st.write("Updated List After Deletion:")
        df.index += 1  # Start index from 1
        st.write(df)
        
        # Show the total amount after deletion
        total_amount = df['Amount'].sum()
        st.write(f"**Total Amount Collected After Deletion:** ₹{total_amount}")
    else:
        st.error(f"Roll No {roll_no} not found.")

# Streamlit app for collecting student data
st.title("Forum Fees Collection")

ensure_csv()  # Ensure the CSV file is ready

# Form to input new student data
with st.form("entry_form"):
    name = st.text_input("Enter Name")
    roll_no = st.text_input("Enter Roll No (mandatory)", max_chars=4)  # Mandatory field
    amount = st.number_input("Enter Amount", value=250)

    submit = st.form_submit_button("Submit")

    if submit:
        # Check if Roll No is provided
        if roll_no.strip() == "":
            st.error("Roll No is mandatory. Please enter a valid Roll No.")
        else:
            append_data(roll_no, name, amount)

# Show the list of data
if st.button("Show List"):
    df = load_data()
    if not df.empty:
        df_sorted = df.sort_values(by='Roll No').reset_index(drop=True)  # Reset index for clean display
        df_sorted.index += 1  # Start the index from 1 instead of 0
        st.write(df_sorted.astype(int))
        
        # Calculate and display total amount
        total_amount = df['Amount'].sum()
        st.write(f"**Amount Collected:** ₹{total_amount}")
        st.write(f"**Amount left:** ₹{(13000-total_amount)}")
        st.write(f"**Total Amount to collect:** ₹{13000}")
        st.write(f"**No. of student left:** {(13000-total_amount)//250}")
    else:
        st.write("No data available.")

# Option to delete a row by roll number
with st.form("delete_form"):
    delete_roll_no = st.text_input("Enter the Roll No to delete")
    delete_submit = st.form_submit_button("Delete")

    if delete_submit:
        delete_row_by_roll_no(delete_roll_no)
