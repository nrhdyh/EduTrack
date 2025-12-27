import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Objective 1 – Demographics Analysis",
    layout="wide"
)

st.title("Objective 1: Demographic & Academic Factors Influencing GPA")

# ==================================================
# LOAD DATA FROM GOOGLE SHEETS (PUBLIC CSV)
# ==================================================
@st.cache_data
def load_data():
    sheet_id = "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw"
    gid = "0"  # ⚠️ Change this if Cleaned_data has a different gid

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# Load data safely
try:
    df = load_data()
    st.success("✅ Data loaded successfully from Google Sheets")
except Exception as e:
    st.error("❌ Failed to load data from Google Sheets")
    st.exception(e)
    st.stop()

# ==================================================
# DATA CLEANING
# ==================================================
df["GPA"] = pd.to_numeric(df["GPA"], errors="coerce")
df["YearStudy"] = pd.to_numeric(df["YearStudy"], errors="coerce")

df["Attendance"] = pd.to_numeric(
    df["Attendance"].astype(str).str.replace("%", "", regex=False),
    errors="coerce"
)

df = df.dropna(subset=["GPA"])

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.header("Filters")

year_options = sorted(df["YearStudy"].dropna().unique())
faculty_options = sorted(df["Faculty"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Year of Study",
    year_options,
    default=year_options
)

selected_faculties = st.sidebar.multiselect(
    "Faculty",
    faculty_options,
    default=faculty_options
)

df = df[
    (df["YearStudy"].isin(selected_years)) &
    (df["Faculty"].isin(selected_faculties))
]

# ==================================================
# VISUAL SETTINGS
# ==================================================
sns.set(style="whitegrid")

# ==================================================
# 1. BAR CHART – AVG GPA BY GENDER
# ==================================================
st.subheader("1. Average GPA by Gender")

fig, ax = plt.subplots()
sns.barplot(data=df, x="Gender", y="GPA", errorbar=None, ax=ax)
ax.set_title("Average GPA by Gender")
st.pyplot(fig)

# ==================================================
# 2. BOX PLOT – GPA BY YEAR OF STUDY
# ==================================================
st.subheader("2. GPA Distribution by Year of Study")

fig, ax = plt.subplots()
sns.boxplot(data=df, x="YearStudy", y="GPA", ax=ax)
ax.set_title("GPA Distribution by Year of Study")
st.pyplot(fig)

# ==================================================
# 3. BAR CHART – AVG GPA BY FACULTY
# ==================================================
st.subheader("3. Average GPA by Faculty")

fig, ax = plt.subplots(figsize=(10, 5))
faculty_order = (
    df.groupby("Faculty")["GPA"]
    .mean()
    .sort_values(ascending=False)
    .index
)

sns.barplot(
    data=df,
    x="Faculty",
    y="GPA",
    order=faculty_order,
    errorbar=None,
    ax=ax
)

ax.set_title("Average GPA by Faculty")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
st.pyplot(fig)

# ==================================================
# 4. SCATTER – ATTENDANCE VS GPA
# ==================================================
st.subheader("4. Attendance Percentage vs GPA")

fig, ax = plt.subplots()
sns.scatterplot(
    data=df,
    x="Attendance",
    y="GPA",
    hue="YearStudy",
    ax=ax
)
ax.set_title("Attendance Percentage vs GPA")
st.pyplot(fig)

# ==================================================
# 5. BOX PLOT – SCHOLARSHIP VS GPA
# ==================================================
st.subheader("5. Scholarship Status vs GPA")

fig, ax = plt.subplots()
sns.boxplot(data=df, x="Scholarship", y="GPA", ax=ax)
ax.set_title("Scholarship Status vs GPA")
st.pyplot(fig)

# ==================================================
# 6. HEATMAP – YEAR × FACULTY VS GPA
# ==================================================
st.subheader("6. Heatmap: Year of Study × Faculty vs Average GPA")

pivot = df.pivot_table(
    values="GPA",
    index="YearStudy",
    columns="Faculty",
    aggfunc="mean"
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax)
ax.set_title("Year of Study × Faculty vs Average GPA")
st.pyplot(fig)

# ==================================================
# 7. LINE CHART – GPA TREND ACROSS YEARS
# ==================================================
st.subheader("7. GPA Trend Across Years of Study")

yearly_gpa = (
    df.groupby("YearStudy")["GPA"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots()
sns.lineplot(
    data=yearly_gpa,
    x="YearStudy",
    y="GPA",
    marker="o",
    ax=ax
)
ax.set_title("GPA Trend Across Years of Study")
st.pyplot(fig)

# ==================================================
# DATA PREVIEW
# ==================================================
with st.expander("View Cleaned Data"):
    st.dataframe(df)

# ==================================================
# SUMMARY METRIC
# ==================================================
st.metric("Total Responses", len(df))

