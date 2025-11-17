# app.py
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="Survey Dashboard", layout="wide")

# --- Authentication to Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
# Use secrets from .streamlit/secrets.toml for service_account json
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scopes=scope
)
client = gspread.authorize(creds)

# Sheet info
SHEET_ID = "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw"
WORKSHEET_NAME = "Form Responses 1"  # adjust if different

sheet = client.open_by_key(SHEET_ID)
worksheet = sheet.worksheet(WORKSHEET_NAME)

# --- Read existing data ---
data = worksheet.get_all_values()
headers = data[0]
rows = data[1:]
df = pd.DataFrame(rows, columns=headers)

st.title("📊 Student Performance Survey Dashboard")

st.markdown("### Current responses")
st.dataframe(df)

st.markdown("---")

st.markdown("### Submit your response")

# --- Build a form for user submission ---
with st.form("survey_form", clear_on_submit=True):
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.selectbox("Age (Years)", ["19-20", "21-22", "23-25", "26-28", "29+"])
    # … add more fields matching your Google Form/Sheet  
    previous_gpa = st.text_input("What was your previous GPA?")
    hours_study_daily = st.selectbox("How many hours do you study daily?", ["<1", "1-2", "3-4", "5-6", ">6"])
    # … continue with remaining fields
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        new_row = [
            timestamp,
            gender,
            age,
            previous_gpa,
            hours_study_daily,
            # … include other fields in correct order
        ]
        worksheet.append_row(new_row, value_input_option="USER_ENTERED")
        st.success("Thank you! Your response has been recorded.")
        # optionally reload data
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        st.dataframe(df)

# --- Optional: Some simple stats or charts ---
st.markdown("### Some stats")
if "Age (Years)" in df.columns:
    st.bar_chart(df["Age (Years)"].value_counts())
