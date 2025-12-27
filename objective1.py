import streamlit as st
import pandas as pd

st.set_page_config(page_title="Objective 1 – Demographics Analysis", layout="wide")
st.title("Objective 1: Demographic & Academic Factors Influencing GPA")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    sheet_id = "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw"
    gid = "0"  # Replace if Cleaned_data tab has different gid
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

df = load_data()
st.success("✅ Data loaded successfully")

# ----------------------------
# DATA CLEANING
# ----------------------------
df["GPA"] = pd.to_numeric(df["GPA"], errors="coerce")
df["YearStudy"] = pd.to_numeric(df["YearStudy"], errors="coerce")
df["Attendance"] = pd.to_numeric(df["Attendance"].astype(str).str.replace("%", "", regex=False), errors="coerce")
df = df.dropna(subset=["GPA"])

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")
selected_years = st.sidebar.multiselect("Year of Study", sorted(df["YearStudy"].unique()), default=sorted(df["YearStudy"].unique()))
selected_faculties = st.sidebar.multiselect("Faculty", sorted(df["Faculty"].unique()), default=sorted(df["Faculty"].unique()))
df = df[(df["YearStudy"].isin(selected_years)) & (df["Faculty"].isin(selected_faculties))]

# ----------------------------
# 1. AVG GPA BY GENDER
# ----------------------------
st.subheader("1. Average GPA by Gender")
gender_mean = df.groupby("Gender")["GPA"].mean()
st.bar_chart(gender_mean)

# ----------------------------
# 2. GPA BY YEAR OF STUDY
# ----------------------------
st.subheader("2. GPA Distribution by Year of Study")
yearly_gpa = df.groupby("YearStudy")["GPA"].mean()
st.line_chart(yearly_gpa)

# ----------------------------
# 3. AVG GPA BY FACULTY
# ----------------------------
st.subheader("3. Average GPA by Faculty")
faculty_mean = df.groupby("Faculty")["GPA"].mean()
st.bar_chart(faculty_mean)

# ----------------------------
# 4. ATTENDANCE VS GPA
# ----------------------------
st.subheader("4. Attendance vs GPA")
st.scatter_chart = df[['Attendance','GPA']]  # Streamlit 1.28+ supports st.scatter_chart()
st.write(st.scatter_chart)

# ----------------------------
# 5. SCHOLARSHIP VS GPA
# ----------------------------
st.subheader("5. Scholarship Status vs GPA")
scholarship_mean = df.groupby("Scholarship")["GPA"].mean()
st.bar_chart(scholarship_mean)

# ----------------------------
# DATA PREVIEW
# ----------------------------
with st.expander("View Cleaned Data"):
    st.dataframe(df)

st.metric("Total Responses", len(df))
