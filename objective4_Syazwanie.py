import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="EduTrack Performance Dashboard",
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
# THEME STYLE (SOFT BLUE / PURPLE)
# ---------------------------------------
block_style = """
    background: linear-gradient(135deg, #6A85B6, #B993D6);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
"""

# ---------------------------------------
# TITLE & OVERVIEW
# ---------------------------------------
st.title("🎓 Student Performance & Skill Development Analytics")
st.markdown("""
This dashboard explores the relationship between students’ academic performance,
skill development, and co-curricular involvement among UMK students.
""")
st.markdown("---")

# ---------------------------------------
# FILTER SECTION
# ---------------------------------------
st.subheader("🔍 Dashboard Filters")

f1, f2, f3 = st.columns(3)
with f1:
    year_filter = st.selectbox("Year of Study", ["All"] + sorted(df["Year_of_Study"].dropna().unique()))
with f2:
    skill_filter = st.selectbox("Skill Development Level", ["All"] + sorted(df["Skill_Development_Hours_Category"].dropna().unique()))
with f3:
    cocur_filter = st.selectbox("Co-Curricular Participation", ["All"] + sorted(df["Co_Curriculum_Activities_Text"].dropna().unique()))

filtered_df = df.copy()
if year_filter != "All":
    filtered_df = filtered_df[filtered_df["Year_of_Study"] == year_filter]
if skill_filter != "All":
    filtered_df = filtered_df[filtered_df["Skill_Development_Hours_Category"] == skill_filter]
if cocur_filter != "All":
    filtered_df = filtered_df[filtered_df["Co_Curriculum_Activities_Text"] == cocur_filter]

# ---------------------------------------
# KPI SUMMARY
# ---------------------------------------
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
# 1️⃣ Performance Density (KDE)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ CGPA Density: Active vs Non-Active Students</h3></div>', unsafe_allow_html=True)

active = filtered_df[filtered_df['Co_Curriculum_Activities_Text'] == 'Yes']['CGPA_Midpoint'].dropna()
inactive = filtered_df[filtered_df['Co_Curriculum_Activities_Text'] == 'No']['CGPA_Midpoint'].dropna()

fig1 = ff.create_distplot(
    [active, inactive],
    ['Active', 'Non-Active'],
    show_hist=False,
    show_rug=False,
    colors=['#6A85B6', '#B993D6']
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# 2️⃣ Average CGPA by Skill & Co-Curricular
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Skill Development & Co-Curricular</h3></div>', unsafe_allow_html=True)

df_grouped = filtered_df.groupby(
    ['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text']
)['CGPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    df_grouped,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    barmode='group',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3️⃣ CGPA Percentage Distribution
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
    percentage_dist,
    y='Skills_Category',
    x='Percentage',
    color='CGPA_Range',
    orientation='h',
    text=percentage_dist['Percentage'].round(1),
    color_discrete_sequence=px.colors.sequential.PuBu
)
st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# 4️⃣ Split Violin Plot
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ CGPA Distribution: Skill vs Co-Curricular</h3></div>', unsafe_allow_html=True)

fig4 = go.Figure()

fig4.add_trace(go.Violin(
    x=filtered_df['Skill_Development_Hours_Category'][filtered_df['Co_Curriculum_Activities_Text'] == 'Yes'],
    y=filtered_df['CGPA_Midpoint'][filtered_df['Co_Curriculum_Activities_Text'] == 'Yes'],
    name='Active',
    side='positive',
    line_color='#6A85B6',
    meanline_visible=True
))

fig4.add_trace(go.Violin(
    x=filtered_df['Skill_Development_Hours_Category'][filtered_df['Co_Curriculum_Activities_Text'] == 'No'],
    y=filtered_df['CGPA_Midpoint'][filtered_df['Co_Curriculum_Activities_Text'] == 'No'],
    name='Non-Active',
    side='negative',
    line_color='#B993D6',
    meanline_visible=True
))

fig4.update_layout(violinmode='overlay')
st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# 5️⃣ CGPA Progression Line Chart
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ CGPA Progression by Year & Skill Level</h3></div>', unsafe_allow_html=True)

df_line = filtered_df.groupby(
    ['Year_of_Study', 'Skill_Development_Hours_Category']
)['CGPA_Midpoint'].mean().reset_index()

fig5 = px.line(
    df_line,
    x='Year_of_Study',
    y='CGPA_Midpoint',
    color='Skill_Development_Hours_Category',
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Safe
)
st.plotly_chart(fig5, use_container_width=True)

# =====================================================
# 6️⃣ Heatmap
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>6️⃣ Average CGPA Heatmap</h3></div>', unsafe_allow_html=True)

heatmap_data = filtered_df.pivot_table(
    values='CGPA_Midpoint',
    index='Skill_Development_Hours_Category',
    columns='Co_Curriculum_Activities_Text',
    aggfunc='mean'
)

fig6 = px.imshow(
    heatmap_data,
    text_auto='.2f',
    color_continuous_scale='PuBu',
    aspect='auto'
)
st.plotly_chart(fig6, use_container_width=True)

# =====================================================
# 7️⃣ Academic Consistency
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>7️⃣ Academic Consistency: GPA vs CGPA</h3></div>', unsafe_allow_html=True)

df_melted = filtered_df.melt(
    id_vars=['Co_Curriculum_Activities_Text'],
    value_vars=['GPA_Midpoint', 'CGPA_Midpoint'],
    var_name='Metric',
    value_name='Score'
)

df_consistency = df_melted.groupby(
    ['Co_Curriculum_Activities_Text', 'Metric']
)['Score'].mean().reset_index()

fig7 = px.bar(
    df_consistency,
    x='Co_Curriculum_Activities_Text',
    y='Score',
    color='Metric',
    barmode='group',
    text_auto='.2f',
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig7.update_layout(yaxis_range=[3.0, 3.7])
st.plotly_chart(fig7, use_container_width=True)

st.caption("🔵🟣 UMK EduTrack Analytics Dashboard")
