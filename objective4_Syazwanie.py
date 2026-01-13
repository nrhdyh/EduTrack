import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="EduTrack Academic Performance Dashboard",
    layout="wide"
)

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance_ver2.csv"
    return pd.read_csv(url)

df = load_data()

# ---------------------------------------
# THEME STYLE (SOFT BLUE–PURPLE)
# ---------------------------------------
block_style = """
background: linear-gradient(135deg, #667eea, #764ba2);
color: white;
padding: 22px;
border-radius: 14px;
text-align: center;
box-shadow: 2px 4px 12px rgba(0,0,0,0.12);
"""

section_style = """
background: #f6f7fb;
padding: 22px;
border-radius: 14px;
"""
interpretation_style = """
background: linear-gradient(135deg, #f3e8ff, #ede9fe);
padding: 20px;
border-radius: 14px;
margin-top: 12px;
color: #2e1065;
box-shadow: 1px 3px 10px rgba(0,0,0,0.08);
"""

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title("🎓 EduTrack: The Impact of Skill Development and Co-curricular Engagement on Academic Performance")
st.markdown("---")

# =====================================================
# 📌 PROBLEM STATEMENT
# =====================================================
st.markdown("## 📌 Problem Statement")
st.markdown(f"""
<div style="{section_style}">
Despite consistent academic assessment through GPA and CGPA, the influence of 
<b>skill development</b> and <b>co-curricular participation</b> on students’ academic 
performance is not clearly understood. Without data-driven insights, universities 
may struggle to identify effective strategies for supporting academic excellence 
and early intervention for at-risk students.
</div>
""", unsafe_allow_html=True)

# =====================================================
# 🎯 OBJECTIVE
# =====================================================
st.markdown("## 🎯 Research Objective")
st.markdown(f"""
<div style="{section_style}">
To analyze how <b>skill development levels</b> and <b>co-curricular participation</b> 
influence students’ academic performance (CGPA) using visual analytics.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------
# 📄 DATASET PREVIEW (MATCH FRIEND STYLE)
# ---------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())
st.markdown("---")

# =====================================================
# 🔍 FILTERS
# =====================================================
st.subheader("🔍 Dashboard Filters")

c1, c2, c3 = st.columns(3)
with c1:
    year = st.selectbox("Year of Study", ["All"] + sorted(df["Year_of_Study"].dropna().unique()))
with c2:
    skill = st.selectbox("Skill Development Level", ["All"] + sorted(df["Skill_Development_Hours_Category"].dropna().unique()))
with c3:
    cocur = st.selectbox("Co-Curricular Participation", ["All"] + sorted(df["Co_Curriculum_Activities_Text"].dropna().unique()))

filtered_df = df.copy()
if year != "All":
    filtered_df = filtered_df[filtered_df["Year_of_Study"] == year]
if skill != "All":
    filtered_df = filtered_df[filtered_df["Skill_Development_Hours_Category"] == skill]
if cocur != "All":
    filtered_df = filtered_df[filtered_df["Co_Curriculum_Activities_Text"] == cocur]

# =====================================================
# 📊 KPI SUMMARY
# =====================================================
avg_gpa = filtered_df["GPA_Midpoint"].mean()
avg_cgpa = filtered_df["CGPA_Midpoint"].mean()
total_students = len(filtered_df)
active_rate = (filtered_df["Co_Curriculum_Activities_Text"] == "Yes").mean() * 100

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div style="{block_style}"><h5>Total Students</h5><h2>{total_students}</h2></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div style="{block_style}"><h5>Average GPA</h5><h2>{avg_gpa:.2f}</h2></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div style="{block_style}"><h5>Average CGPA</h5><h2>{avg_cgpa:.2f}</h2></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div style="{block_style}"><h5>Active Participation</h5><h2>{active_rate:.1f}%</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 1️⃣ KDE – CGPA Density
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ CGPA Density: Active vs Non-Active Students</h3></div>', unsafe_allow_html=True)

active = filtered_df[filtered_df['Co_Curriculum_Activities_Text'] == 'Yes']['CGPA_Midpoint'].dropna()
inactive = filtered_df[filtered_df['Co_Curriculum_Activities_Text'] == 'No']['CGPA_Midpoint'].dropna()

fig1 = ff.create_distplot(
    [active, inactive],
    ['Active Students', 'Non-Active Students'],
    show_hist=False,
    show_rug=False,
    colors=['#667eea', '#764ba2']
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(f"""
<div style="{interpretation_style}">
<b>🔍 What the Visual Shows</b><br>
The KDE density plot compares the distribution and concentration of CGPA between students 
who participate in co-curricular activities and those who do not.<br><br>

<b>🧠 Analysis</b><br>
Visually, both groups display a normal distribution peaking at the 3.3 to 3.4 CGPA mark,
but an anomaly emerges at the upper tail, where active students have a considerably higher
concentration in the 3.8 to 4.0 range. This trend demonstrates that participation in campus activities
has no negative effect on grades; rather, it suggests a link in which high-achieving students are more
likely to be involved in their community.As a result, the case study's setting is reinforced, as an
active lifestyle is frequently a trademark of disciplined, top-tier UMK students rather than a
distraction from their academics.<br><br>

<b>🎯 Why This Matters</b><br>
Rather than focusing only on mean CGPA, this visualization highlights risk dispersion. 
Students who are not involved in structured activities may be more vulnerable to academic 
fluctuation, even if their average CGPA appears acceptable.
</div>
""", unsafe_allow_html=True)

# =====================================================
# 2️⃣ Grouped Bar – Avg CGPA
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Skill Development & Co-Curricular</h3></div>', unsafe_allow_html=True)

grouped = filtered_df.groupby(
    ['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text']
)['CGPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    grouped,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"""
<div style="{interpretation_style}">
<b>🔍 What the Visual Shows</b><br>
The grouped bar chart compares average CGPA midpoints across different skill development levels, 
separated by co-curricular participation status. serving to identify the interactive effect of
 two distinct lifestyle factors on academic success<br><br>

<b>🧠 Analysis</b><br>
The visual data shows that for the "High" skill category, participation in activities leads
to a higher CGPA (~3.55), but for the "Medium" category, those involved in activities perform
significantly worse than their non-active peers.This reveals a trend in which high-performing
students have the stronger time-management ability to thrive under numerous responsibilities,
whereas moderate-performers experience academic dilution when overcommitted.<br><br>

<b>🎯 Why This Matters</b><br>
This conclusion relates back to the original dilemma by showing that the benefits of a
"active" lifestyle are dependent on a student's baseline academic efficiency and workload
capacity
</div>
""", unsafe_allow_html=True)

# =====================================================
# 3️⃣ CGPA Distribution (Percentage-Based)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Distribution by Skills Category</h3></div>', unsafe_allow_html=True)

cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']

cross_tab = pd.crosstab(filtered_df['Skills_Category'], filtered_df['CGPA'])
cross_tab = cross_tab[[c for c in cgpa_order if c in cross_tab.columns]]

percentage = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage = percentage.reset_index().melt(
    id_vars='Skills_Category',
    var_name='CGPA_Range',
    value_name='Percentage'
)

fig3 = px.bar(
    percentage,
    y='Skills_Category',
    x='Percentage',
    color='CGPA_Range',
    orientation='h',
    text=percentage['Percentage'].round(1),
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown(f"""
<div style="{interpretation_style}">
<b>🔍 What the Visual Shows</b><br>
A 100% stacked bar chart is utilized to analyze the proportional composition of CGPA ranges
within various skill categories, allowing for a direct comparison of academic performance
tiers across diverse learning interests.<br><br>

<b>🧠 Analysis</b><br>
The visual evidence indicates a surprising anomaly: the "Hardware & Technical Support" group
is entirely made up of students with the lowest CGPA (2.50-2.99), although "Soft Skills" and
"Office & Engineering Tools" are dominated by high-tier students (44.4% and 50%, respectively).
This pattern demonstrates a clear link between high academic standing and the pursuit of
adaptable, professional skills, whereas lower-achieving students appear to prefer towards
specialised, manual technical niches.<br><br>

<b>🎯 Why This Matters</b><br>
This conclusion is relevant to the problem context because it suggests that academic capability
influences the strategic selection of market-ready abilities, with higher-performing students
emphasising leadership and tool-based competency.
</div>
""", unsafe_allow_html=True)

# =====================================================
# 4️⃣ Line Chart – Academic Progression
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ CGPA Progression by Year & Skill Level</h3></div>', unsafe_allow_html=True)

line_data = filtered_df.groupby(
    ['Year_of_Study', 'Skill_Development_Hours_Category']
)['CGPA_Midpoint'].mean().reset_index()

fig4 = px.line(
    line_data,
    x='Year_of_Study',
    y='CGPA_Midpoint',
    color='Skill_Development_Hours_Category',
    markers=True
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown(f"""
<div style="{interpretation_style}">
<b>🔍 What the Visual Shows</b><br>
The multi-series line graph effectively tracks the progression of CGPA midpoints from Year 1
to Year 4, categorized by skill development intensity to highlight longitudinal trends and
performance sustainability<br><br>

<b>🧠 Analysis</b><br>
A critical anomaly is noted in which students with "High" skill development hours begin at
the highest midpoint of 3.85 in Year 1 but fall sharply and consistently to 3.45 by Year 4,
whereas "Low" intensity students demonstrate a steady upward recovery. This decreasing trend
indicates a "burnout" effect, in which the initial high-intensity investment in skill
development becomes unsustainable when core academic rigour increases in the senior years. <br><br>

<b>🎯 Why This Matters</b><br>
 This finding addresses the original problem context of students' long-term academic stability,
 implying that excessive early-stage commitment to external talents may later jeopardise degree
 achievement.
</div>
""", unsafe_allow_html=True)


# =====================================================
# 5️⃣ Heatmap – Decision Matrix
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ Average CGPA Heatmap</h3></div>', unsafe_allow_html=True)

heatmap_data = filtered_df.pivot_table(
    values='CGPA_Midpoint',
    index='Skill_Development_Hours_Category',
    columns='Co_Curriculum_Activities_Text',
    aggfunc='mean'
)

fig5 = px.imshow(
    heatmap_data,
    text_auto='.2f',
    color_continuous_scale='PuBu',
    aspect='auto'
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown(f"""
<div style="{interpretation_style}">
<b>🔍 What the Visual Shows</b><br>
The correlation heatmap uses color-coded intensity to represent precise CGPA averages at
the intersection of skill hours and co-curricular engagement, providing a clear visual
matrix of performance "sweet spots" and risk zones.<br><br>

<b>🧠 Analysis</b><br>
The data show a maximum average of 3.57 for the "High Skill/Yes Activity" cohort and
a minimum of 3.37 for the "Medium Skill/Yes Activity" group, with the latter having
the lowest academic yield across the entire dataset. This visual data demonstrates a
robust relationship between focused, high-intensity involvement and peak academic results,
while also highlighting "moderate" engagement as a unique risk factor for performance decreases.<br><br>

<b>🎯 Why This Matters</b><br>
Finally, this supports the research context by demonstrating that academic performance
at UMK is driven by the deliberate, high-level integration of lifestyle elements rather
than simply the availability of activities themselves.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("---")
st.caption("🔵🟣 EduTrack Visual Analytics | UMK Student Performance")
