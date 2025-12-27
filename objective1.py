import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Objective 1 – Demographics Analysis",
    layout="wide"
)

st.title("Objective 1: Demographic & Academic Factors Influencing GPA")

# ==================================================
# LOAD DATA FROM PUBLISHED CSV
# ==================================================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTfh2K4-xu0yFkoRoOHxcEA4-CrRxZMNfe5EiflGI0OTLJUraozJV3Gp5sijGN8dVYyNOP29T5Fm39F/pub?gid=680023838&single=true&output=csv"
    return pd.read_csv(url)

try:
    df = load_data()
    st.success("✅ Data loaded successfully")
except Exception as e:
    st.error("❌ Failed to load data")
    st.exception(e)
    st.stop()

# ==================================================
# DATA CLEANING
# ==================================================
df["GPA"] = pd.to_numeric(df["GPA"], errors="coerce")
df["YearStudy"] = pd.to_numeric(df["YearStudy"], errors="coerce")
df["Attendance"] = pd.to_numeric(df["Attendance"].astype(str).str.replace("%", "", regex=False), errors="coerce")
df = df.dropna(subset=["GPA"])

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.header("Filters")
selected_years = st.sidebar.multiselect("Year of Study", sorted(df["YearStudy"].unique()), default=sorted(df["YearStudy"].unique()))
selected_faculties = st.sidebar.multiselect("Faculty", sorted(df["Faculty"].unique()), default=sorted(df["Faculty"].unique()))
df = df[(df["YearStudy"].isin(selected_years)) & (df["Faculty"].isin(selected_faculties))]

# ==================================================
# 1. BAR CHART – AVG GPA BY GENDER
# ==================================================
st.subheader("1. Average GPA by Gender")
gender_mean = df.groupby("Gender")["GPA"].mean().reset_index()
fig1 = px.bar(gender_mean, x="Gender", y="GPA", title="Average GPA by Gender", text="GPA")
st.plotly_chart(fig1, use_container_width=True)

# ==================================================
# 2. BOX PLOT – GPA BY YEAR OF STUDY
# ==================================================
st.subheader("2. GPA Distribution by Year of Study")
fig2 = px.box(df, x="YearStudy", y="GPA", title="GPA Distribution by Year of Study")
st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# 3. BAR CHART – AVG GPA BY FACULTY
# ==================================================
st.subheader("3. Average GPA by Faculty")
faculty_mean = df.groupby("Faculty")["GPA"].mean().reset_index().sort_values(by="GPA", ascending=False)
fig3 = px.bar(faculty_mean, x="Faculty", y="GPA", title="Average GPA by Faculty", text="GPA")
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# 4. SCATTER – ATTENDANCE VS GPA
# ==================================================
st.subheader("4. Attendance Percentage vs GPA")
fig4 = px.scatter(df, x="Attendance", y="GPA", color="YearStudy", title="Attendance Percentage vs GPA")
st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# 5. BOX PLOT – SCHOLARSHIP VS GPA
# ==================================================
st.subheader("5. Scholarship Status vs GPA")
fig5 = px.box(df, x="Scholarship", y="GPA", title="Scholarship Status vs GPA")
st.plotly_chart(fig5, use_container_width=True)

# ==================================================
# 6. HEATMAP – YEAR × FACULTY VS GPA
# ==================================================
st.subheader("6. Heatmap: Year × Faculty vs Average GPA")
pivot = df.pivot_table(values="GPA", index="YearStudy", columns="Faculty", aggfunc="mean").reset_index()
fig6 = go.Figure(data=go.Heatmap(
    z=pivot.drop('YearStudy', axis=1).values,
    x=pivot.columns[1:],
    y=pivot['YearStudy'],
    colorscale='YlGnBu',
    text=pivot.drop('YearStudy', axis=1).values,
    hovertemplate='Year: %{y}<br>Faculty: %{x}<br>GPA: %{z:.2f}<extra></extra>'
))
fig6.update_layout(title="Year × Faculty vs Average GPA")
st.plotly_chart(fig6, use_container_width=True)

# ==================================================
# 7. LINE CHART – GPA TREND ACROSS YEARS
# ==================================================
st.subheader("7. GPA Trend Across Years of Study")
yearly_gpa = df.groupby("YearStudy")["GPA"].mean().reset_index()
fig7 = px.line(yearly_gpa, x="YearStudy", y="GPA", markers=True, title="GPA Trend Across Years of Study")
st.plotly_chart(fig7, use_container_width=True)

# ==================================================
# DATA PREVIEW
# ==================================================
with st.expander("View Cleaned Data"):
    st.dataframe(df)

st.metric("Total Responses", len(df))
