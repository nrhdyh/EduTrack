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

# ---------------------------------------
# HELPER FUNCTION (FIX HEATMAP ISSUE)
# ---------------------------------------
def sort_by_lower_bound(value):
    try:
        return float(value.split("-")[0].strip().replace("%", ""))
    except:
        return 0

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title("🎓 Demographic Characteristics and Academic Factors Influencing UMK Students Performance")
st.markdown("""Academic performance is a key indicator of student success, yet it is influenced by a combination of demographic characteristics and academic factors. 
At Universiti Malaysia Kelantan (UMK), students come from diverse backgrounds in terms of gender, age, races, and relationship status, while also differing in academic-related behaviors such as participation in co-curricular activities, attendance, and CGPA/GPA. 
Despite the availability of such data, there is limited research analyzing how these factors collectively affect student performance. Without this understanding, it is challenging for university stakeholders to design effective interventions and support programs. 
Therefore, this study seeks to examine the relationship between demographic and academic factors and student performance at UMK, with the aim of identifying key predictors of academic success to guide strategies for improving student outcomes.""")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
df = pd.read_csv(url)

# ---------------------------------------
# DATA PREVIEW
# ---------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())
st.markdown("---")

# =====================================================
# 📊 SUMMARY INSIGHT BOXES
# =====================================================
avg_cgpa = df["CGPA_Midpoint"].mean()

top_faculty = (
    df.groupby("Faculty_Short")["CGPA_Midpoint"]
    .mean()
    .idxmax()
)

cgpa_gpa_corr = df["CGPA_Midpoint"].corr(df["GPA_Midpoint"])
common_living = df["Living_With"].mode()[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("📈 Average CGPA", f"{avg_cgpa:.2f}")
col2.metric("🏆 Top Faculty (Avg CGPA)", top_faculty)
col3.metric("🔗 CGPA–GPA Correlation", f"{cgpa_gpa_corr:.2f}")
col4.metric("🏠 Common Living Arrangement", common_living)

st.markdown("---")


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
st.markdown("---")

# =====================================================
# 2️⃣ Histogram: GPA by Relationship Status & Gender (Dropdown)
# =====================================================
st.subheader("2️⃣ GPA Distribution by Relationship Status and Gender")

relationship_options = df["Relationship_Status"].dropna().unique()
selected_relationship = st.selectbox(
    "Select Relationship Status",
    relationship_options
)

filtered_df = df[df["Relationship_Status"] == selected_relationship]

fig_hist = px.histogram(
    filtered_df,
    x="GPA_Midpoint",
    color="Gender",
    barmode="overlay",
    opacity=0.7,
    title=f"GPA Distribution by Gender ({selected_relationship})"
)

st.plotly_chart(fig_hist, use_container_width=True)
st.markdown("---")

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
st.markdown("---")

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
st.markdown("---")

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
st.markdown("---")

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
st.markdown("---")

# =====================================================
# 7️⃣ Heatmap: Study Hours vs Attendance (by Living With)
# =====================================================
st.subheader("7️⃣ Heatmap: Study Hours vs Attendance by Living Arrangement")

study_order = sorted(
    df["Study_Hours_Daily"].dropna().unique(),
    key=sort_by_lower_bound
)

attendance_order = sorted(
    df["Attendance_Percentage"].dropna().unique(),
    key=sort_by_lower_bound
)

living_options = df["Living_With"].dropna().unique()
selected_living = st.selectbox(
    "Select Living Arrangement",
    living_options
)

subset = df[df["Living_With"] == selected_living]

pivot = subset.pivot_table(
    index="Study_Hours_Daily",
    columns="Attendance_Percentage",
    values="CGPA_Midpoint",
    aggfunc="mean"
)

pivot = pivot.reindex(index=study_order, columns=attendance_order)

fig_heatmap = px.imshow(
    pivot,
    text_auto=".2f",
    color_continuous_scale="Viridis",
    aspect="auto",
    title=f"Average CGPA by Study Hours & Attendance ({selected_living})"
)

fig_heatmap.update_layout(
    xaxis_title="Attendance Percentage",
    yaxis_title="Daily Study Hours"
)

st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("---")

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

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("### 📌 Conclusion")
st.markdown(
    "This dashboard provides interactive visual insights into how demographic, academic, "
    "and socio-economic factors influence student academic performance."
)
