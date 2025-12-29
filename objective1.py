import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

st.title("🎓 Student Performance Analysis Dashboard")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
df = pd.read_csv(url)

st.subheader("Dataset Preview")
st.dataframe(df.head())

# =====================================================
# 1️⃣ Violin Plot: CGPA by Gender
# =====================================================
st.subheader("1️⃣ CGPA Distribution by Gender")

fig_violin = px.violin(
    df,
    x="Gender",
    y="CGPA_Midpoint",
    box=True,
    points="all",
    color="Gender",
    title="Violin Plot of CGPA Midpoint by Gender"
)

st.plotly_chart(fig_violin, use_container_width=True)

# =====================================================
# 2️⃣ Faceted Histogram: GPA by Relationship Status & Gender
# =====================================================
st.subheader("2️⃣ GPA Distribution by Relationship Status and Gender")

fig_hist = px.histogram(
    df,
    x="GPA_Midpoint",
    color="Gender",
    facet_col="Relationship_Status",
    facet_col_wrap=3,
    barmode="overlay",
    opacity=0.7,
    title="Distribution of GPA Midpoint by Relationship Status and Gender"
)

st.plotly_chart(fig_hist, use_container_width=True)

# =====================================================
# 3️⃣ Bar Chart: Average CGPA by Faculty
# =====================================================
st.subheader("3️⃣ Average CGPA by Faculty")

fig_faculty = px.bar(
    df,
    x="Faculty_Short",
    y="CGPA_Midpoint",
    color="Faculty_Short",
    title="Average CGPA Midpoint by Faculty"
)

fig_faculty.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_faculty, use_container_width=True)

# =====================================================
# 4️⃣ Scatter Plot: CGPA vs Age
# =====================================================
st.subheader("4️⃣ Relationship Between CGPA and Age")

fig_age = px.scatter(
    df,
    x="CGPA_Midpoint",
    y="Age_Midpoint",
    trendline="ols",
    title="Scatter Plot of CGPA vs Age"
)

st.plotly_chart(fig_age, use_container_width=True)

# =====================================================
# 5️⃣ Line Chart: CGPA vs GPA by Year of Study
# =====================================================
st.subheader("5️⃣ CGPA Trend by GPA and Year of Study")

line_data = (
    df.groupby(["GPA_Midpoint", "Year_of_Study"])["CGPA_Midpoint"]
    .mean()
    .reset_index()
)

fig_line = px.line(
    line_data,
    x="GPA_Midpoint",
    y="CGPA_Midpoint",
    color="Year_of_Study",
    markers=True,
    title="Average CGPA by GPA Midpoint and Year of Study"
)

st.plotly_chart(fig_line, use_container_width=True)

# =====================================================
# 6️⃣ Bar Chart: CGPA by Family Income
# =====================================================
st.subheader("6️⃣ Average CGPA by Family Income")

fig_income = px.bar(
    df,
    x="Family_Income",
    y="CGPA_Midpoint",
    color="Family_Income",
    title="Average CGPA Midpoint by Family Income"
)

fig_income.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_income, use_container_width=True)

# =====================================================
# 7️⃣ Complex Heatmaps: Study Hours vs Attendance (by Living With)
# =====================================================
st.subheader("7️⃣ Heatmap: Study Hours vs Attendance by Living Arrangement")

def sort_by_lower_bound(val):
    if pd.isna(val):
        return np.inf
    val = str(val)
    if val.startswith(">"):
        return float(val[1:])
    return float(val.split("-")[0])

study_order = sorted(df["Study_Hours_Daily"].dropna().unique(), key=sort_by_lower_bound)
attendance_order = sorted(df["Attendance_Percentage"].dropna().unique(), key=sort_by_lower_bound)

living_options = df["Living_With"].dropna().unique()
selected_living = st.selectbox("Select Living Arrangement", living_options)

subset = df[df["Living_With"] == selected_living]

pivot = subset.pivot_table(
    index="Study_Hours_Daily",
    columns="Attendance_Percentage",
    values="CGPA_Midpoint",
    aggfunc="mean"
).reindex(index=study_order, columns=attendance_order)

fig_heatmap = px.imshow(
    pivot,
    text_auto=".2f",
    color_continuous_scale="Viridis",
    title=f"Average CGPA by Study Hours & Attendance ({selected_living})"
)

fig_heatmap.update_layout(
    xaxis_title="Attendance Percentage",
    yaxis_title="Daily Study Hours"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# =====================================================
# 8️⃣ Bubble Chart: GPA & CGPA by Race
# =====================================================
st.subheader("8️⃣ Bubble Chart: GPA & CGPA by Race")

fig_bubble = px.scatter(
    df,
    x="CGPA_Midpoint",
    y="Races",
    size="GPA_Midpoint",
    color="GPA_Midpoint",
    color_continuous_scale="Viridis",
    title="Bubble Chart of GPA and CGPA by Race",
    size_max=40
)

st.plotly_chart(fig_bubble, use_container_width=True)
