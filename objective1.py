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
st.markdown("""Academic performance is influenced by both demographic and academic factors. 
At Universiti Malaysia Kelantan (UMK), students vary in gender, age, race, and relationship status, as well as in academic behaviors attendance and CGPA/GPA. 
However, limited research examines how these factors collectively impact student performance, making it difficult for stakeholders to design effective support programs. 
This study aims to explore these relationships to identify key predictors of academic success and guide strategies to improve student outcomes.""")
st.markdown("---")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
df = pd.read_csv(url)

# =====================================================
# 📊 SUMMARY INSIGHT BOXES
# =====================================================

st.subheader("📊 Key Summary Insights")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    selected_gender = st.selectbox(
        "Filter by Gender",
        ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    )

with col_f2:
    selected_faculty = st.selectbox(
        "Filter by Faculty",
        ["All"] + sorted(df["Faculty_Short"].dropna().unique().tolist())
    )

with col_f3:
    selected_living = st.selectbox(
        "Filter by Living Arrangement",
        ["All"] + sorted(df["Living_With"].dropna().unique().tolist())
    )

# Apply filters
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

if selected_faculty != "All":
    filtered_df = filtered_df[filtered_df["Faculty_Short"] == selected_faculty]

if selected_living != "All":
    filtered_df = filtered_df[filtered_df["Living_With"] == selected_living]

# Compute metrics dynamically
avg_cgpa = filtered_df["CGPA_Midpoint"].mean()
top_faculty = (
    filtered_df.groupby("Faculty_Short")["CGPA_Midpoint"]
    .mean()
    .idxmax()
    if not filtered_df.empty else "N/A"
)

cgpa_gpa_corr = (
    filtered_df["CGPA_Midpoint"].corr(filtered_df["GPA_Midpoint"])
    if len(filtered_df) > 1 else 0
)

common_living = (
    filtered_df["Living_With"].mode()[0]
    if not filtered_df.empty else "N/A"
)
st.markdown("---")
# Display metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("📈 Average CGPA", f"{avg_cgpa:.2f}")
col2.metric("🏆 Top Faculty", top_faculty)
col3.metric("🔗 CGPA–GPA Correlation", f"{cgpa_gpa_corr:.2f}")
col4.metric("🏠 Common Living", common_living)

st.markdown("---")

# ---------------------------------------
# DATA PREVIEW
# ---------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())
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

# =====================================================
# Interactive Analysis Controls
# =====================================================
st.markdown("### 🔍 Interactive Analysis Options")

show_stats = st.checkbox("Summary Statistics by Gender", value=True)
show_interpretation = st.checkbox("Interpretation", value=True)
show_conclusion = st.checkbox("Conclusion", value=True)

# =====================================================
# Summary Statistics
# =====================================================
if show_stats:
    st.markdown("### 📊 Summary Statistics")
    stats_df = (
        df.groupby("Gender")["CGPA_Midpoint"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
    )
    st.dataframe(stats_df, use_container_width=True)

# =====================================================
# Interpretation Section
# =====================================================
if show_interpretation:
    st.markdown("""
### 📈 Interpretation

The violin plot illustrates the distribution of CGPA midpoints for male and female students, highlighting differences in central tendency, spread, and density.

Both genders show CGPA values primarily concentrated between **3.2 and 3.6**, indicating strong overall academic performance. Female students demonstrate a **slightly higher median CGPA**, suggesting marginally better average academic outcomes.

Female CGPA values exhibit **greater variability**, indicating a broader range of performance, including a higher presence of top achievers. In contrast, male students display a **more compact distribution**, reflecting more consistent performance within a narrower CGPA range.

A small number of **lower-end CGPA outliers** are observed for both genders, likely reflecting individual academic challenges rather than a systematic gender effect.
""")

# =====================================================
# Scientific Conclusion (Dynamic)
# =====================================================
if show_conclusion:
    female_mean = df[df["Gender"] == "Female"]["CGPA_Midpoint"].mean()
    male_mean = df[df["Gender"] == "Male"]["CGPA_Midpoint"].mean()

    st.markdown("### 🧪 Conclusion")

    if female_mean > male_mean:
        st.success(
            f"Female students show a higher average CGPA ({female_mean:.2f}) "
            f"compared to male students ({male_mean:.2f}). "
            "This suggests a modest association between gender and academic performance."
        )
    else:
        st.info(
            f"Male students show a higher or comparable average CGPA "
            f"({male_mean:.2f}) compared to female students ({female_mean:.2f}). "
            "This suggests minimal gender-based differences in academic performance."
        )

    st.markdown("""
Despite observable differences in central tendency, the substantial overlap between distributions indicates that
**gender alone is not a strong predictor of academic success**. Other academic and socio-environmental factors are likely more influential.
""")

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
# =====================================================
# 6️⃣ Bar Chart: CGPA by Income Category
# =====================================================
st.subheader("6️⃣ Average CGPA by Income Category")

fig_income = px.bar(
    df,
    x="Income_Category",
    y="CGPA_Midpoint",
    color="Income_Category",
    title="Average CGPA Midpoint by Income Category"
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
