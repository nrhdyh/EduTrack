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
st.title("🎓 EduTrack: Academic Performance & Student Development Dashboard")
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
The density curve for active students is more concentrated around higher CGPA values, 
indicating greater academic consistency. In contrast, non-active students exhibit a wider 
spread, suggesting higher variability and academic instability. This indicates that 
co-curricular participation does not merely increase average performance, but reduces 
performance volatility, which is crucial for sustaining academic outcomes over time.<br><br>

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
The grouped bar chart compares average CGPA across different skill development levels, 
separated by co-curricular participation status.<br><br>

<b>🧠 Analysis</b><br>
A clear upward trend is observed as skill development increases. More importantly, within 
each skill category, students who actively participate in co-curricular activities 
consistently outperform their non-active peers. This demonstrates a reinforcement effect: 
skill development improves academic performance, but its impact is amplified when combined 
with active engagement beyond the classroom.<br><br>

<b>🎯 Why This Matters</b><br>
This suggests that academic success is multidimensional. Universities focusing solely on 
academic instruction may overlook the compounding benefits of experiential learning and 
structured student engagement.
</div>
""", unsafe_allow_html=True)

# =====================================================
# 3️⃣ CGPA Distribution (Percentage-Based)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Distribution by Skills Category</h3></div>', unsafe_allow_html=True)

cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']

cross_tab = pd.crosstab(filtered_df['Skills_Category'], filtered_df['CGPA'])
cross_tab = cross_tab[[c for c in cgpa_order if c in cross_tab.columns]]

percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage_dist = percentage_dist.reset_index().melt(
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
This stacked percentage bar chart illustrates how students are distributed across CGPA 
ranges within each skill category.<br><br>

<b>🧠 Analysis</b><br>
High-skill students dominate the top CGPA range (3.70–4.00), while low-skill groups show a 
higher concentration in mid and lower CGPA bands. This proportional view reveals academic 
risk concentration, which is not visible through averages alone. The visualization clearly 
distinguishes between performance excellence and performance vulnerability, highlighting 
where academic support mechanisms should be targeted.<br><br>

<b>🎯 Why This Matters</b><br>
This chart shifts the focus from “how well students perform” to “how many students are at 
risk”, enabling more strategic academic planning.
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
The line chart tracks CGPA trends across academic years for different skill development 
levels.<br><br>

<b>🧠 Analysis</b><br>
Students with medium and high skill development exhibit stable or improving CGPA 
trajectories, while low-skill students show flatter or inconsistent patterns. This suggests 
that skill development contributes not only to short-term performance, but also to academic 
sustainability over time. As academic complexity increases in higher years, students without 
adequate skill development may struggle to maintain performance.<br><br>

<b>🎯 Why This Matters</b><br>
The visualization emphasizes the importance of early skill investment, particularly in 
lower academic years, to prevent long-term academic decline.
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
The heatmap presents average CGPA across combinations of skill development levels and 
co-curricular participation.<br><br>

<b>🧠 Analysis</b><br>
The highest CGPA values are concentrated in the high-skill & active participation quadrant, 
while the lowest values appear in the low-skill & non-active group. This confirms a 
synergistic relationship between skill development and co-curricular involvement, where 
neither factor alone produces optimal academic outcomes.<br><br>

<b>🎯 Why This Matters</b><br>
The heatmap functions as a decision-support tool, clearly identifying student profiles that 
are thriving versus those that require intervention.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("---")
st.caption("🔵🟣 EduTrack Visual Analytics | UMK Student Performance")
