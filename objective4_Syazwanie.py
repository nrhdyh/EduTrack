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

st.markdown("""
**Interpretation & Analysis:**  
The density plot reveals that students who actively participate in co-curricular activities 
display a more concentrated CGPA distribution at higher values, indicating stronger academic 
consistency. In contrast, non-active students show wider dispersion, suggesting greater 
performance variability and academic risk. This highlights that co-curricular participation 
supports not only higher achievement but also stability in academic outcomes.
""")

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

st.markdown("""
**Interpretation & Analysis:**  
The visualization demonstrates a clear positive relationship between skill development 
and CGPA. Across all skill categories, students who actively engage in co-curricular 
activities consistently achieve higher academic performance. This suggests a reinforcement 
effect, where skill development enhances academic capability, and co-curricular engagement 
amplifies its impact.
""")

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
    color_discrete_sequence=px.colors.sequential.PuBu
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
**Interpretation & Analysis:**  
The stacked percentage bar chart highlights a strong concentration of high-skill students
within the top CGPA range (3.70–4.00), while low-skill groups are disproportionately 
represented in mid and lower CGPA bands. Unlike average-based views, this proportional 
analysis exposes academic risk concentration, clearly distinguishing between performance
excellence and vulnerability. The visualization therefore provides a more strategic lens
for identifying student groups that require targeted academic support.
""")

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

st.markdown("""
**Interpretation & Analysis:**  
The line chart illustrates that students with medium and high skill development maintain
stable or improving CGPA trajectories across academic years, whereas low-skill students
display flatter or more inconsistent patterns. This trend suggests that skill development
contributes to long-term academic sustainability, particularly as coursework complexity
increases in later years. Early investment in student skill development is therefore
critical to preventing cumulative academic decline.
""")

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

st.markdown("""
**Interpretation & Analysis:**  
The heatmap shows that the highest average CGPA values are concentrated among students
with high skill development who actively participate in co-curricular activities, while
the lowest performance is observed in low-skill, non-active students. This pattern confirms
a synergistic relationship between skill development and engagement, where optimal academic
outcomes emerge only when both factors are present. As a result, the heatmap serves as an
effective decision-support tool for identifying both high-performing and at-risk student
profile
""")

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("---")
st.caption("🔵🟣 EduTrack Visual Analytics | UMK Student Performance")
