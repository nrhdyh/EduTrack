import streamlit as st
import pandas as pd
import plotly.express as px
# import numpy as np

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

#---------------------------------------
# TITLE
#---------------------------------------
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
# 📊 SUMMARY INSIGHT BLOCK BOXES
# =====================================================
st.subheader("📊 Key Summary Insights")

# Filters
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

# Compute metrics
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

# Display metrics in block boxes
col1, col2, col3, col4 = st.columns(4)

background-color:#6A1B9A;
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);

with col1:
    st.markdown(f'<div style="{block_style}"><h3>📈 Average CGPA</h3><p style="font-size:20px; font-weight:bold;">{avg_cgpa:.2f}</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div style="{block_style}"><h3>🏆 Top Faculty</h3><p style="font-size:20px; font-weight:bold;">{top_faculty}</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div style="{block_style}"><h3>🔗 CGPA–GPA Correlation</h3><p style="font-size:20px; font-weight:bold;">{cgpa_gpa_corr:.2f}</p></div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div style="{block_style}"><h3>🏠 Common Living</h3><p style="font-size:20px; font-weight:bold;">{common_living}</p></div>', unsafe_allow_html=True)

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
# Compact Display Options
# =====================================================
# st.markdown("---")

show_stats = st.checkbox("Summary Statistics", value=True, key="compact_stats")
show_description = st.checkbox("Distribution Description", value=True, key="compact_desc")


# =====================================================
# Summary Statistics (Descriptive Only)
# =====================================================
if show_stats:
    st.markdown("### 📊 Summary Statistics by Gender")

    stats_df = (
        df.groupby("Gender")["CGPA_Midpoint"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
    )

    st.dataframe(stats_df, use_container_width=True)

# =====================================================
# Distribution Description (Neutral)
# =====================================================
if show_description:
    st.markdown("""
### 📈 Distribution Description

The violin plot displays the distribution of CGPA midpoints for male and female students, showing the shape, spread, and concentration of values for each group.

CGPA values for both genders are distributed within a similar overall range, with areas of higher density where values occur more frequently. The distributions overlap across most of the CGPA range.

Variation in the width of the violins reflects differences in data concentration at specific CGPA levels. A small number of observations appear at the lower and upper ends of the distributions, indicating less frequent CGPA values.
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

# =====================================================
# Analysis Options (Optional Display Only)
# =====================================================
# st.markdown("### 🔍 Display Options")

show_stats_2 = st.checkbox("Summary Statistics", value=True, key="stats2")
show_interpretation_2 = st.checkbox("Distribution Description", value=True, key="desc2")

# =====================================================
# Summary Statistics (Descriptive)
# =====================================================
if show_stats_2:
    st.markdown("### 📊 Summary Statistics by Gender")

    stats_df_2 = (
        filtered_df.groupby("Gender")["GPA_Midpoint"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
    )

    st.dataframe(stats_df_2, use_container_width=True)

# =====================================================
# Distribution Description (Neutral Only)
# =====================================================
if show_interpretation_2:
    st.markdown(f"""
### 📈 Distribution Description

The histogram displays the frequency distribution of GPA midpoints by gender for students with **{selected_relationship}** relationship status.

GPA values for both genders are spread across a similar range, with overlapping bars observed across most GPA intervals. Differences in bar height indicate variations in the number of observations within each GPA bin.

The distribution shapes show areas of higher concentration where GPA values occur more frequently, as well as lower-frequency intervals. No distinct separation between gender-based distributions is visually apparent within this relationship category.
""")

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

# =====================================================
# Display Options
# =====================================================
# st.markdown("### 🔍 Display Options")

show_stats_3 = st.checkbox("Average CGPA Table", value=True, key="stats3")
show_description_3 = st.checkbox("Distribution Description", value=True, key="desc3")

# =====================================================
# Average CGPA Table (Descriptive)
# =====================================================
if show_stats_3:
    st.markdown("### 📊 Average CGPA by Faculty")

    faculty_avg = (
        df.groupby("Faculty_Short")["CGPA_Midpoint"]
        .mean()
        .reset_index(name="Average_CGPA")
    )

    st.dataframe(faculty_avg, use_container_width=True)

# =====================================================
# Description (Neutral Only)
# =====================================================
if show_description_3:
    st.markdown("""
### 📈 Distribution Description

The bar chart displays the average CGPA midpoint for each faculty, allowing comparison of mean CGPA values across academic faculties.

Differences in bar height reflect variation in average CGPA midpoints among faculties. Some faculties show higher average values while others display lower averages within the overall CGPA range observed in the dataset.

The chart summarizes central tendency at the faculty level and does not reflect individual student-level variation within each faculty.
""")

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

# =====================================================
# Display Options
# =====================================================
# st.markdown("### 🔍 Display Options")

show_stats_4 = st.checkbox("Summary Statistics", value=True, key="stats4")
show_description_4 = st.checkbox("Distribution Description", value=True, key="desc4")

# =====================================================
# Summary Statistics (Descriptive)
# =====================================================
if show_stats_4:
    st.markdown("### 📊 Summary Statistics")

    age_cgpa_stats = (
        df[["CGPA_Midpoint", "Age_Midpoint"]]
        .describe()
        .reset_index()
    )

    st.dataframe(age_cgpa_stats, use_container_width=True)

# =====================================================
# Distribution Description (Neutral Only)
# =====================================================
if show_description_4:
    st.markdown("""
### 📈 Distribution Description

The scatter plot displays individual data points representing CGPA midpoints plotted against age midpoints.

Points are spread across the CGPA range with variation in age values, showing how observations are distributed across both variables. The fitted trendline provides a visual reference for the general direction of the data without indicating the strength or significance of the relationship.

The dispersion of points around the trendline indicates variability in CGPA values across different ages, with no single age group dominating the distribution.
""")

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

# =====================================================
# Display Options
# =====================================================
# st.markdown("### 🔍 Display Options")

show_stats_5 = st.checkbox("Summary Statistics", value=True, key="stats5")
show_description_5 = st.checkbox("Distribution Description", value=True, key="desc5")

# =====================================================
# Summary Statistics (Descriptive)
# =====================================================
if show_stats_5:
    st.markdown("### 📊 Summary Statistics")

    cgpa_gpa_stats = (
        line_data[["GPA_Midpoint", "CGPA_Midpoint"]]
        .describe()
        .reset_index()
    )

    st.dataframe(cgpa_gpa_stats, use_container_width=True)

# =====================================================
# Distribution Description (Neutral Only)
# =====================================================
if show_description_5:
    st.markdown(""" 
### 📈 Distribution Description

The line chart shows average CGPA values for each GPA midpoint, separated by year of study.  

Lines indicate the distribution of CGPA averages across GPA midpoints, with each year represented by a separate line, showing how observations are spread without implying trends or effects.
""")

st.markdown("---")


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

# =====================================================
# Display Options
# =====================================================
# st.markdown("### 🔍 Display Options")

show_stats_6 = st.checkbox("Summary Statistics", value=True, key="stats6")
show_description_6 = st.checkbox("Distribution Description", value=True, key="desc6")

# =====================================================
# Summary Statistics (Descriptive)
# =====================================================
if show_stats_6:
    st.markdown("### 📊 Summary Statistics")

    cgpa_income_stats = (
        df.groupby("Income_Category")["CGPA_Midpoint"]
        .describe()
        .reset_index()
    )

    st.dataframe(cgpa_income_stats, use_container_width=True)

# =====================================================
# Distribution Description (Neutral Only)
# =====================================================
if show_description_6:
    st.markdown(""" 
### 📈 Distribution Description

The bar chart displays average CGPA midpoints for each income category.  

Bars represent the spread of CGPA values across categories, showing differences in averages without implying cause or effect.
""")

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

# =====================================================
# Display Options
# =====================================================
# st.markdown("### 🔍 Display Options")

show_stats_7 = st.checkbox("Summary Statistics", value=True, key="stats7")
show_description_7 = st.checkbox("Distribution Description", value=True, key="desc7")

# =====================================================
# Summary Statistics (Descriptive)
# =====================================================
if show_stats_7:
    st.markdown("### 📊 Summary Statistics")

    study_attendance_stats = (
        pivot.stack().describe().reset_index().rename(columns={0: "CGPA_Midpoint"})
    )

    st.dataframe(study_attendance_stats, use_container_width=True)

# =====================================================
# Distribution Description (Neutral Only)
# =====================================================
if show_description_7:
    st.markdown(""" 
### 📈 Distribution Description

The heatmap shows average CGPA values for combinations of daily study hours and attendance percentages, filtered by living arrangement.  

Color intensity represents the distribution of CGPA values across these combinations, without implying causation or trends.
""")

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

# =====================================================
# Display Options
# =====================================================
# st.markdown("### 🔍 Display Options")

show_stats_8 = st.checkbox("Summary Statistics", value=True, key="stats8")
show_description_8 = st.checkbox("Distribution Description", value=True, key="desc8")

# =====================================================
# Summary Statistics (Descriptive)
# =====================================================
if show_stats_8:
    st.markdown("### 📊 Summary Statistics")

    bubble_stats = (
        df.groupby("Races")[["CGPA_Midpoint", "GPA_Midpoint"]]
        .describe()
        .reset_index()
    )

    st.dataframe(bubble_stats, use_container_width=True)

# =====================================================
# Distribution Description (Neutral Only)
# =====================================================
if show_description_8:
    st.markdown(""" 
### 📈 Distribution Description

The bubble chart displays CGPA midpoints on the x-axis and race categories on the y-axis, with bubble size representing GPA midpoints.  

Bubbles indicate the distribution of GPA and CGPA values across races, without implying trends or causal relationships.
""")

st.markdown("---")

# # ---------------------------------------
# # FOOTER
# # ---------------------------------------
# st.markdown(
#     "This dashboard provides interactive visual insights into how demographic, academic, "
#     "and socio-economic factors influence student academic performance."
# )
