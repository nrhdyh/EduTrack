import streamlit as st
import pandas as pd
import plotly.express as px
# import numpy as np

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Demographic",
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
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance_ver2.csv"
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

# Define the block style as a string
block_style = """
    background: linear-gradient(135deg, #5E35B1, #3949AB);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
"""

# Display metrics in block boxes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div style="{block_style}"><h5>📈 Average CGPA</h5><p style="font-size:20px; font-weight:bold;">{avg_cgpa:.2f}</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div style="{block_style}"><h5>🏆 Top Faculty</h5><p style="font-size:20px; font-weight:bold;">{top_faculty}</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div style="{block_style}"><h5>🔗 CGPA–GPA Correlation</h5><p style="font-size:20px; font-weight:bold;">{cgpa_gpa_corr:.2f}</p></div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div style="{block_style}"><h5>🏠 Common Living</h5><p style="font-size:20px; font-weight:bold;">{common_living}</p></div>', unsafe_allow_html=True)

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
st.markdown(f"""
<div style="{block_style}">
    <h3>1️⃣ Violin Plot: CGPA Distribution by Gender</h3>
</div>
""", unsafe_allow_html=True)

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

# 🔹 Natural visual break
st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================
# Summary Statistics (Descriptive Only)
# =====================================================
st.markdown("### 📊 Summary Statistics")

show_stats = st.checkbox("Show summary statistics", value=True, key="compact_stats")
if show_stats:
    stats_df = (
        df.groupby("Gender")["CGPA_Midpoint"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
    )
    st.dataframe(stats_df, use_container_width=True)

# 🔹 Natural visual break
st.markdown("<br><br>", unsafe_allow_html=True)

# =====================================================
# Distribution Description (Neutral)
# =====================================================
st.markdown("### 📈 Distribution Description")

show_description = st.checkbox("Show distribution description", value=True, key="compact_desc")
if show_description:
    st.markdown("""
- Female students tend to achieve slightly higher CGPA scores, with results more concentrated
    in the upper CGPA range, indicating greater consistency. 
- Male students show a wider spread
    of CGPA values, suggesting higher variability. 
- Overall, the pattern indicates a moderate
    relationship between gender and academic performance.
    """)


st.markdown("---")

# =====================================================
# 2️⃣ Histogram: GPA by Relationship Status & Gender (Dropdown)
# =====================================================
st.markdown(f"""
<div style="{block_style}">
    <h3>2️⃣ Histogram: GPA Distribution by Relationship Status and Gender</h3>
</div>
""", unsafe_allow_html=True)


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
# Summary Statistics (Descriptive)
# =====================================================
show_stats_2 = st.checkbox("Summary Statistics", value=True, key="stats2")
if show_stats_2:
    st.markdown("### 📊 Summary Statistics by Gender")

    stats_df_2 = (
        filtered_df.groupby("Gender")["GPA_Midpoint"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
    )

    st.dataframe(stats_df_2, use_container_width=True)

# =====================================================
# Distribution Description (Storytelling Style)
# =====================================================
show_interpretation_2 = st.checkbox("Distribution Description", value=True, key="desc2")

if show_interpretation_2:
    if selected_relationship.lower() == "single":
        st.markdown(f"""
### 📈 Distribution Description

- For students who are **single**, the GPA distribution shows the widest spread across the scale.
Most observations cluster around the mid-range GPA values, forming a clear central pattern,
while a noticeable extension into higher GPA bins suggests that a subset of students performs particularly well.

- Female students appear more frequently in the higher GPA ranges, whereas male students are more concentrated
around the central bins. 

- Despite this, substantial overlap remains between genders, indicating shared academic
patterns rather than strong gender separation. No extreme outliers or abrupt gaps are observed.
""")

    elif selected_relationship.lower() == "in a relationship":
        st.markdown(f"""
### 📈 Distribution Description

- Among students **in a relationship**, GPA values are distributed mainly from mid to high ranges,
with both genders showing a balanced and stable pattern.
The overlapping bars across most GPA intervals suggest similar academic engagement between males and females.

- Female students show a slightly stronger presence in the higher GPA bins, though the difference is gradual
and not sharply pronounced. 

- The overall shape reflects consistency, with no clear anomalies or sudden
declines in performance.
""")

    elif selected_relationship.lower() == "married":
        st.markdown(f"""
### 📈 Distribution Description

- For **married** students, the GPA distribution appears more concentrated, with values clustering toward
the higher end of the GPA scale. The narrower spread suggests stable and focused academic outcomes.

- Both genders display nearly identical patterns, and no notable gaps or anomalies are present.
Although the sample size is smaller, the distribution indicates consistency rather than variability.
""")

    else:
        st.markdown(f"""
### 📈 Distribution Description

- The GPA distribution for students with **{selected_relationship}** status shows overlapping patterns
between genders, with GPA values concentrated within similar ranges.
No distinct anomalies or separations are visually evident.
""")

st.markdown("---")

# =====================================================
# 3️⃣ Line Chart: CGPA vs GPA by Year of Study
# =====================================================
st.markdown(f"""
<div style="{block_style}">
    <h3>️3️⃣ Line Chart: CGPA Trend by GPA and Year of Study</h3>
</div>
""", unsafe_allow_html=True)


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
# Summary Statistics (Descriptive)
# =====================================================
show_stats_5 = st.checkbox("Summary Statistics", value=True, key="stats5")
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
show_description_5 = st.checkbox("Distribution Description", value=True, key="desc5")
if show_description_5:
    st.markdown(""" 
### 📈 Distribution Description

As students progress through their academic journey, their CGPA seems to tell a quiet story of growth and resilience.
- 1st year students begin modestly, hovering around a CGPA of 2.9 at a GPA midpoint of 2.8. But as GPA increases, their CGPA rises gradually, slow and steady.
- 2nd year there are something shifts. With the same GPA midpoint, their CGPA climbs higher and reaching 3.45 at a GPA midpoint of 3.4. It’s as if they finally understand the rhythm of university life.
- 3rd year tells the most compelling chapter. Students do not just improve but they soar. At a GPA midpoint of 3.8, 3rd year students record the highest CGPA of all, brushing close to 3.85 and the mark of academic maturity, confidence and refined study habits.
- 4th year is the final stretch. Their trend mirrors Year 2, but slightly lower than 3rd year, suggesting that  final-year pressures, projects and internships slow down the climb just a little.

Overall, the plot reveals a clear pattern:
- Higher GPA generally correlates with higher CGPA
- Each year of study tends to increase performance
**The standout anomaly 3rd year outperforming even 4th year get the hints that academic peak may occur before graduation, when focus is strongest and external pressures are fewer.
""")

st.markdown("---")


# =====================================================
# 4️⃣ Bar Chart: CGPA by Income Category
# =====================================================
st.markdown(f"""
<div style="{block_style}">
    <h3>️4️⃣ Bar Chart: Average CGPA by Income Category</h3>
</div>
""", unsafe_allow_html=True)


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
# Summary Statistics (Descriptive)
# =====================================================
show_stats_6 = st.checkbox("Summary Statistics", value=True, key="stats6")
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
show_description_6 = st.checkbox("Distribution Description", value=True, key="desc6")
if show_description_6:
    st.markdown(""" 
### 📈 Distribution Description

Across the university environment, academic performance often reflects more than just study habits because it can mirror student's backgrounds and circumstances. 
In this chart, the story unfolds through three groups: B40, M40, and T20.
* **B40**: Students with household income **below RM1,500** or between **RM1,501 and RM3,000**
* **M40**: Students with household income between **RM3,001 and RM5,000** or **RM5,001 and RM8,000**
* **T20**: Students with household income between **RM8,001 and RM12,000** or **above RM12,000**

- The M40 students stand tallest, with the highest average CGPA midpoint. It’s as if they sit at a balance point—supported enough to focus fully on studies, yet driven by the hunger to climb higher.
- Close behind are the B40 students. Despite having fewer financial resources, they show remarkable academic strength are almost matching the M40. Their achievement hints at resilience, determination, and perhaps stronger motivation to change their circumstances.
- T20 group surprisingly lower in performance. Their bar rests noticeably shorter, as if academic pressure or external commitments have shifted their priorities. Unlike the others, performance may not be the sole focus and comfort and opportunity might offer them more paths beyond grades.

The pattern whispers a simple truth:
Academic excellence doesn’t always belong to those with the most wealth sometimes, it shines brightest where the drive to succeed burns strongest.
""")

st.markdown("---")


# =====================================================
# 5️⃣ Heatmap: Study Hours vs Attendance (by Living With)
# =====================================================
st.markdown(f"""
<div style="{block_style}">
    <h3>5️⃣ Heatmap: Study Hours vs Attendance by Living Arrangement</h3>
</div>
""", unsafe_allow_html=True)


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
# Summary Statistics (Descriptive)
# =====================================================
show_stats_7 = st.checkbox("Summary Statistics", value=True, key="stats7")
if show_stats_7:
    st.markdown("### 📊 Summary Statistics")

    study_attendance_stats = (
        pivot.stack().describe().reset_index().rename(columns={0: "CGPA_Midpoint"})
    )

    st.dataframe(study_attendance_stats, use_container_width=True)

# =====================================================
# Distribution Description (Dynamic Based On Selection)
# =====================================================
show_description_7 = st.checkbox("Distribution Description", value=True, key="desc7")
if show_description_7:
    st.markdown("### 📈 Distribution Description")

    if selected_living == "Friends":
        st.markdown("""
**Students living with friends show a clear, predictable pattern.**
- Higher study hours combined with higher attendance generally lead to higher CGPA.
- The strongest results appear around **5–6 hours of study with 81–100% attendance**.
- There are no extreme highs or lows — outcomes remain stable, suggesting a balanced, supportive environment that encourages steady academic effort.

**Overall conclusion:** More study + better attendance = reliably higher CGPA.
""")

    elif selected_living == "Family":
        st.markdown("""
**For students living with family, attendance is the defining factor.**
- High attendance (81–100%) consistently produces strong CGPAs (~3.5), even among those studying **less than 1 hour per day**.
- However, low attendance sharply reduces performance, even when study hours increase.

**Overall conclusion:** Showing up matters most — attendance has stronger impact than study time.
""")

    elif selected_living == "In Hostel":
        st.markdown("""
**Hostel life shows the widest academic range — from highest to lowest CGPA.**
- Low attendance and low study hours (e.g., <1 hour + 41–60%) correlate with the lowest scores (~2.75), while high attendance paired with 5–6 study hours produces **the highest CGPA in the dataset (3.85)**.
- This suggests freedom and fewer constraints can boost success — or enable failure.

**Overall conclusion:** High-risk, high-reward environment — outcomes are amplified.
""")

    elif selected_living == "Alone":
        st.markdown("""
**No usable pattern can be identified — the heatmap is empty for this group.**
- This suggests either very few students live alone or the distribution is too scattered to create a meaningful aggregate view.

**Overall conclusiont:** Lack of data = no identifiable trend (which itself is important).
""")

    else:
        st.markdown("""
No descriptive pattern available for this living arrangement.
""")

st.markdown("---")

# =====================================================
#  6️⃣ Bar Chart: Average CGPA by Faculty
# =====================================================
st.markdown(f"""
<div style="{block_style}">
    <h3>6️⃣ Bar Chart: Average CGPA by Faculty</h3>
</div>
""", unsafe_allow_html=True)


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
# Average CGPA Table (Descriptive)
# =====================================================
show_stats_3 = st.checkbox("Average CGPA Table", value=True, key="stats3")
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
show_description_3 = st.checkbox("Distribution Description", value=True, key="desc3")
if show_description_3:
    st.markdown("""
### 📈 Distribution Description

The chart tells a clear and slightly surprising story. 
- One faculty, FSDK, stands far above the rest, creating a strong imbalance in the average CGPA midpoint. 
- This sharp contrast because of the most questionnaire answers are from FSDK students. 
- In contrast, the remaining faculties cluster at much lower and relatively similar levels, indicating more consistent academic performance across them. 
- Faculties such as FPV and FAE show slightly higher midpoints within this cluster, while FBI and FSB sit at the lower end. 
Overall, the dominant anomaly of FSDK overshadows any clear correlation among the other faculties, highlighting the need to analyze it separately to better understand underlying academic trends.
""")

st.markdown("---")

# =====================================================
# 7️⃣ Scatter Plot: CGPA vs Age (With Age Slider)
# =====================================================

st.markdown(f"""
<div style="{block_style}">
    <h3>7️⃣ Scatter Plot: Relationship Between CGPA and Age</h3>
</div>
""", unsafe_allow_html=True)

# =====================================================
# 🎚️ Age Slider Filter
# =====================================================
min_age = int(df["Age_Midpoint"].min())
max_age = int(df["Age_Midpoint"].max())

age_range = st.slider(
    "🎚️ Select Age Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age),
    key="age_slider"
)

# Filter dataset based on selected age range
filtered_df = df[
    (df["Age_Midpoint"] >= age_range[0]) &
    (df["Age_Midpoint"] <= age_range[1])
]

# =====================================================
# 📌 Scatter Plot
# =====================================================
fig_age = px.scatter(
    filtered_df,
    x="CGPA_Midpoint",
    y="Age_Midpoint",
    trendline="ols",
    title=f"Scatter Plot of CGPA vs Age (Age {age_range[0]}–{age_range[1]})",
    labels={
        "CGPA_Midpoint": "CGPA",
        "Age_Midpoint": "Age"
    }
)

st.plotly_chart(fig_age, use_container_width=True)

# =====================================================
# 📊 Summary Statistics (Descriptive)
# =====================================================
show_stats_4 = st.checkbox("Summary Statistics", value=True, key="stats4")
if show_stats_4:
    st.markdown("### 📊 Summary Statistics")

    age_cgpa_stats = (
        filtered_df[["CGPA_Midpoint", "Age_Midpoint"]]
        .describe()
        .reset_index()
    )

    st.dataframe(age_cgpa_stats, use_container_width=True)

# =====================================================
# 📈 Distribution Description (Neutral Only)
# =====================================================
show_description_4 = st.checkbox("Distribution Description", value=True, key="desc4")
if show_description_4:
    st.markdown("""
### 📈 Distribution Description
The scatter plot illustrates the relationship between CGPA and age across the selected age range. 
- Data points are widely dispersed, indicating that students of different ages tend to achieve similar CGPA levels.
- The regression trend line shows a weak and slightly negative association, suggesting that age has minimal influence on CGPA.
- High and low CGPA values appear across multiple age groups, highlighting consistent academic performance regardless of age.
Overall, age does not emerge as a strong predictor of CGPA within the selected range.
""")

st.markdown("---")


# =====================================================
# 8️⃣ Bubble Chart: GPA & CGPA by Race
# =====================================================
st.markdown(f"""
<div style="{block_style}">
    <h3>8️⃣ Bubble Chart: GPA & CGPA by Race</h3>
</div>
""", unsafe_allow_html=True)

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
# Summary Statistics (Descriptive)
# =====================================================
show_stats_8 = st.checkbox("Summary Statistics", value=True, key="stats8")
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
show_description_8 = st.checkbox("Distribution Description", value=True, key="desc8")
if show_description_8:
    st.markdown(""" 
### 📈 Distribution Description

On this chart, each race becomes a character in a shared academic journey for bubble representing both achievement and presence.

- Across most groups, CGPA rises toward the upper end especially around the 3.8 midpoint. 
- The brightest hues and largest bubbles there belong mainly to Malay, Chinese and Indian students showing both stronger GPA and a larger number of students represented. 
- Their bubbles cluster like stars at the high end of the scale, signaling consistent academic strength.

- Further up the chart, Kadazan-Dusun and Bidayuh tell a quieter story. 
- Though not as numerous, their bubbles show that those who are present perform steadily and often falling around the middle CGPA range of 3.4. 
- They may not dominate the numbers, but their performance reflects solid academic standing.

- At the far left, one small single bubble stands out at a CGPA of about 2.8 for the Malay students again, but this variation hints that not all students within a race perform equally. 
- Some struggle, suggesting diversity of outcomes even within the same group.

Overall, the visual speaks softly but clearly:
Academic performance is less about background and more a constellation of individual effort.
""")

st.markdown("---")

# # ---------------------------------------
# # FOOTER
# # ---------------------------------------
# st.markdown(
#     "This dashboard provides interactive visual insights into how demographic, academic, "
#     "and socio-economic factors influence student academic performance."
# )
