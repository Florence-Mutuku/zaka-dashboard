
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="ZAKA Dashboard", layout="centered")
st.title("ZAKA Tithe Contribution System")
st.write("Welcome to the digital ZAKA system!")

# 1) Load existing CSV data (or create an empty DataFrame if file is missing)
csv_path = "zaka_data.csv"
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    df = pd.DataFrame(
        columns=[
            "zaka_number",
            "name",
            "payment_method",
            "amount",
            "timestamp",
            "mpesa_code",
        ]
    )

# 2) Display current contributions
st.subheader(" Current Contributions")
st.dataframe(df, use_container_width=True)

# 3) Entry form for new contribution
st.subheader("➕ Add New Contribution")
with st.form("contribution_form", clear_on_submit=True):
    zaka = st.text_input("ZAKA Number", max_chars=20)
    name = st.text_input("Full Name")
    payment_method = st.selectbox("Payment Method", ["Cash", "Mpesa"])
    amount = st.number_input("Amount (KES)", min_value=1)
    mpesa_code = (
        st.text_input("Mpesa Code (leave blank if Cash)") if payment_method == "Mpesa" else ""
    )
    submitted = st.form_submit_button("Submit Contribution")

    if submitted:
        # Build new record
        new_record = {
            "zaka_number": zaka.strip(),
            "name": name.strip(),
            "payment_method": payment_method,
            "amount": int(amount),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mpesa_code": mpesa_code.strip() if mpesa_code else "",
        }

        # Create a one-row DataFrame for the new record
        new_row_df = pd.DataFrame([new_record])

        # Concatenate it onto the existing DataFrame
        df = pd.concat([df, new_row_df], ignore_index=True)

        # Save the updated DataFrame to CSV
        df.to_csv(csv_path, index=False)

        st.success("✅ Contribution added!")
