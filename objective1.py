import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

st.title("📊 Student Performance Analysis Dashboard")
st.markdown("Demographic & Academic Factors Influencing CGPA")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
df = pd.read_csv(url)

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# --------------------------------------------------
# HELPER FUNCTION FOR SORTING RANGE CATEGORIES
# --------------------------------------------------
def sort_by_lower_bound(val):
    if pd.isna(val):
        return np.inf
    s = str(val).strip()
    if s.startswith(">"):
        return float(s[1:])
    if "-" in s:
        return float(s.split("-")[0])
    return np.inf

# --------------------------------------------------
# 1️⃣ VIOLIN PLOT: Gender vs CGPA
# --------------------------------------------------
st.subheader("1️⃣ CGPA Distribution by Gender")

fig1 = px.violin(
    df,
    x="Gender",
    y="CGPA_Midpoint",
    box=True,
    points="all",
    color="Gender"
)
st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# 2️⃣ BAR CHART: Faculty vs CGPA
# --------------------------------------------------
st.subheader("2️⃣ Average CGPA by Faculty")

faculty_avg = df.groupby("Faculty_Short", as_index=False)["CGPA_Midpoint"].mean()

fig2 = px.bar(
    faculty_avg,
    x="Faculty_Short",
    y="CGPA_Midpoint",
    text_auto=".2f",
    color="Faculty_Short"
)
st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# 3️⃣ SCATTER PLOT: Study Hours vs CGPA
# --------------------------------------------------
st.subheader("3️⃣ Daily Study Hours vs CGPA")

fig3 = px.scatter(
    df,
    x="Study_Hours_Daily",
    y="CGPA_Midpoint",
    color="Gender",
    size="CGPA_Midpoint",
    hover_data=["Faculty_Short"]
)
st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# 4️⃣ BOX PLOT: Attendance vs CGPA
# --------------------------------------------------
st.subheader("4️⃣ CGPA Distribution by Attendance Percentage")

fig4 = px.box(
    df,
    x="Attendance_Percentage",
    y="CGPA_Midpoint",
    color="Attendance_Percentage"
)
st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# 5️⃣ BAR CHART: Family Income vs CGPA
# --------------------------------------------------
st.subheader("5️⃣ Average CGPA by Family Income")

income_order = sorted(df["Family_Income"].dropna().unique(), key=sort_by_lower_bound)

income_avg = df.groupby("Family_Income", as_index=False)["CGPA_Midpoint"].mean()

fig5 = px.bar(
    income_avg,
    x="Family_Income",
    y="CGPA_Midpoint",
    category_orders={"Family_Income": income_order},
    text_auto=".2f",
    color="Family_Income"
)
st.plotly_chart(fig5, use_container_width=True)

# --------------------------------------------------
# 6️⃣ HEATMAP: Study Hours × Attendance
# --------------------------------------------------
st.subheader("6️⃣ Heatmap: Study Hours vs Attendance (Avg CGPA)")

pivot = df.pivot_table(
    index="Study_Hours_Daily",
    columns="Attendance_Percentage",
    values="CGPA_Midpoint",
    aggfunc="mean"
)

study_order = sorted(df["Study_Hours_Daily"].dropna().unique(), key=sort_by_lower_bound)
attendance_order = sorted(df["Attendance_Percentage"].dropna().unique(), key=sort_by_lower_bound)

pivot = pivot.reindex(index=study_order, columns=attendance_order)

fig6 = px.imshow(
    pivot,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="Viridis",
    labels=dict(color="Avg CGPA")
)
st.plotly_chart(fig6, use_container_width=True)

# --------------------------------------------------
# 7️⃣ BUBBLE CHART: Skills × Study Hours
# --------------------------------------------------
st.subheader("7️⃣ Bubble Chart: Skills Category & Study Hours vs CGPA")

bubble_data = (
    df.groupby(["Skills_Category", "Study_Hours_Daily"], as_index=False)
    ["CGPA_Midpoint"]
    .mean()
)

fig7 = px.scatter(
    bubble_data,
    x="Study_Hours_Daily",
    y="Skills_Category",
    size="CGPA_Midpoint",
    color="CGPA_Midpoint",
    size_max=50,
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig7, use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption("Student Performance Dashboard • Streamlit + Plotly")
