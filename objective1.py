import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Objective 1 – Demographics Analysis",
    layout="wide"
)
st.title("Objective 1: Demographic & Academic Factors Influencing GPA")

# ===============================
# LOAD GOOGLE SHEET (GSPREAD)
# ===============================
@st.cache_data
def load_data():
    try:
        # Define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]

        # Load service account credentials
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)

        # Open the sheet and select the tab
        sheet = client.open("EduTrack").worksheet("cleaned_data")  # Change "EduTrack" to your Google Sheet name
        data = sheet.get_all_records()

        df = pd.DataFrame(data)
        return df

    except Exception as e:
        st.error("❌ Failed to load Google Sheet")
        st.exception(e)
        return None

df = load_data()
if df is None:
    st.stop()
st.success("✅ Data loaded successfully")
st.dataframe(df.head())

# ===============================
# DATA CLEANING
# ===============================
df["GPA"] = pd.to_numeric(df["GPA"], errors="coerce")
df["YearStudy"] = pd.to_numeric(df["YearStudy"], errors="coerce")
df["Attendance"] = pd.to_numeric(
    df["Attendance"].astype(str).str.replace("%", "", regex=False),
    errors="coerce"
)
df = df.dropna(subset=["GPA"])

# ===============================
# SIDEBAR FILTERS
# ===============================
st.sidebar.header("Filters")
years = sorted(df["YearStudy"].dropna().unique())
faculties = sorted(df["Faculty"].dropna().unique())

selected_years = st.sidebar.multiselect("Year of Study", years, default=years)
selected_faculties = st.sidebar.multiselect("Faculty", faculties, default=faculties)

df = df[
    (df["YearStudy"].isin(selected_years)) &
    (df["Faculty"].isin(selected_faculties))
]

# ===============================
# VISUAL SETTINGS
# ===============================
sns.set(style="whitegrid")

# ===============================
# 1. BAR CHART – AVG GPA BY GENDER
# ===============================
st.subheader("1. Average GPA by Gender")
fig, ax = plt.subplots()
sns.barplot(data=df, x="Gender", y="GPA", ci=None, ax=ax)
st.pyplot(fig)

# ===============================
# 2. BOX PLOT – GPA BY YEAR
# ===============================
st.subheader("2. GPA Distribution by Year of Study")
fig, ax = plt.subplots()
sns.boxplot(data=df, x="YearStudy", y="GPA", ax=ax)
st.pyplot(fig)

# ===============================
# 3. BAR CHART – GPA BY FACULTY
# ===============================
st.subheader("3. Average GPA by Faculty")
fig, ax = plt.subplots(figsize=(10,5))
order = df.groupby("Faculty")["GPA"].mean().sort_values(ascending=False).index
sns.barplot(data=df, x="Faculty", y="GPA", order=order, ci=None, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
st.pyplot(fig)

# ===============================
# 4. SCATTER – ATTENDANCE VS GPA
# ===============================
st.subheader("4. Attendance Percentage vs GPA")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x="Attendance", y="GPA", hue="YearStudy", ax=ax)
st.pyplot(fig)

# ===============================
# 5. BOX PLOT – SCHOLARSHIP VS GPA
# ===============================
st.subheader("5. Scholarship Status vs GPA")
fig, ax = plt.subplots()
sns.boxplot(data=df, x="Scholarship", y="GPA", ax=ax)
st.pyplot(fig)

# ===============================
# 6. HEATMAP – YEAR × FACULTY
# ===============================
st.subheader("6. Heatmap: Year of Study × Faculty vs GPA")
pivot = df.pivot_table(values="GPA", index="YearStudy", columns="Faculty", aggfunc="mean")
fig, ax = plt.subplots(figsize=(12,6))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# ===============================
# 7. LINE CHART – GPA TREND
# ===============================
st.subheader("7. GPA Trend Across Years of Study")
trend = df.groupby("YearStudy")["GPA"].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=trend, x="YearStudy", y="GPA", marker="o", ax=ax)
st.pyplot(fig)

# ===============================
# DATA PREVIEW
# ===============================
with st.expander("View Cleaned Data"):
    st.dataframe(df)
