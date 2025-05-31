import streamlit as st
import pandas as pd

st.title("Test: Display ZAKA Data")
df = pd.read_csv("zaka_data.csv")
st.dataframe(df)

