import streamlit as st
import pandas as pd

st.title("Survey Submission + Live Data")

st.markdown("### ✏️ Submit your Response")
st.components.v1.iframe(
    "https://docs.google.com/forms/d/e/1FAIpQLSd9hFZX8_o6kSXONBgvT2O0xkzD8Vitltf3Hg3Q8nzguKs5YA/viewform?embedded=true",
    height=800,
)

st.write("---")

st.markdown("### 📊 Real-Time Results")

sheet_url = "https://docs.google.com/spreadsheets/d/1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw/export?format=csv"
df = pd.read_csv(sheet_url)

st.dataframe(df)
