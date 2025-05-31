import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connect or create database
conn = sqlite3.connect('zaka_contributions.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS contributions (
    zaka_number TEXT,
    name TEXT,
    payment_method TEXT,
    amount INTEGER,
    date TEXT,
    mpesa_code TEXT
)
''')
conn.commit()

# Streamlit interface
st.set_page_config(page_title="ZAKA Dashboard", layout="centered")
st.title("ZAKA Tithe Contributions")

# Display current records
st.subheader("📊 All Contributions")
df = pd.read_sql("SELECT * FROM contributions ORDER BY date DESC", conn)
st.dataframe(df, use_container_width=True)

# Add new payment form
st.subheader("➕ Add New Contribution")
with st.form("add_contribution"):
    zaka_number = st.text_input("ZAKA Number")
    name = st.text_input("Full Name")
    payment_method = st.selectbox("Payment Method", ["Cash", "Mpesa"])
    amount = st.number_input("Amount (KES)", min_value=1)
    mpesa_code = st.text_input("Mpesa Code (Leave blank if Cash)")
    submitted = st.form_submit_button("Add Payment")

    if submitted:
        date = datetime.now().strftime("%Y-%m-%d")
        mpesa_code = mpesa_code if payment_method == "Mpesa" else None
        cursor.execute('''
            INSERT INTO contributions VALUES (?, ?, ?, ?, ?, ?)
        ''', (zaka_number, name, payment_method, amount, date, mpesa_code))
        conn.commit()
        st.success("✅ Payment Added Successfully!")

        # Refresh table
        st.experimental_rerun()