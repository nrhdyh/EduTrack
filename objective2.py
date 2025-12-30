import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Academic Performance",
    layout="wide"
)

# ---------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    df = pd.read_csv(url)
    return df

def calculate_hours_midpoint(hours_range):
    if isinstance(hours_range, str):
        cleaned_range = hours_range.replace(' – ', ' - ').replace(' hours', '').replace(' hour', '').strip()
        if ' - ' in cleaned_range:
            lower, upper = map(float, cleaned_range.split(' - '))
            return (lower + upper) / 2
        elif '>' in cleaned_range:
            return float(cleaned_range.replace('>', '')) + 0.5
        elif '<' in cleaned_range:
            return float(cleaned_range.replace('<', '')) - 0.5
    return np.nan

# ---------------------------------------
# LOAD & PRE-PROCESS DATA
# ---------------------------------------
df = load_data()

# Pre-calculate midpoints for metrics and correlation
df['Study_Hours_Daily_Midpoint'] = df['Study_Hours_Daily'].apply(calculate_hours_midpoint)
df['Social_Media_Hours_Daily_Midpoint'] = df['Social_Media_Hours_Daily'].apply(calculate_hours_midpoint)

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title("🎓 Academic Factors Influencing Student Performance")
st.markdown("""
Study habits, social media usage and health factors are aspects of lifestyle that could have influence the academic performance of UMK students.
However, the relationship between these factors and students' academic is still poorly explored through visual analysis. Therefore, this study
aims to visualize and understand the relationship between lifestyle factors and students' academic performance.
""")
st.markdown("---")

# =====================================================
# 📊 SUMMARY INSIGHT BLOCK BOXES
# =====================================================
st.subheader("📊 Key Summary Insights")

# Compute overall metrics
avg_gpa = df["GPA_Midpoint"].mean()
avg_study = df["Study_Hours_Daily_Midpoint"].mean()
avg_social = df["Social_Media_Hours_Daily_Midpoint"].mean()
avg_attendance = df["Attendance_Midpoint"].mean()

# Block Style
block_style = """
    background: linear-gradient(135deg, #5E35B1, #3949AB);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    height: 120px;
"""

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div style="{block_style}"><h4>Average GPA</h4><p style="font-size:22px; font-weight:bold;">{avg_gpa:.2f}</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div style="{block_style}"><h4>Avg Study Hours</h4><p style="font-size:22px; font-weight:bold;">{avg_study:.1f} hrs</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div style="{block_style}"><h4>Avg Social Media</h4><p style="font-size:22px; font-weight:bold;">{avg_social:.1f} hrs</p></div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div style="{block_style}"><h4>Avg Attendance</h4><p style="font-size:22px; font-weight:bold;">{avg_attendance:.1f}%</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 📈 VISUALIZATIONS
# =====================================================

# 1. Study Hours
st.header("1. Average GPA by Study Hours")
study_gpa = df.groupby('Study_Hours_Category')['GPA_Midpoint'].mean().reset_index()
fig1 = px.bar(
    study_gpa, x='Study_Hours_Category', y='GPA_Midpoint', color='Study_Hours_Category',
    category_orders={'Study_Hours_Category': ['Low', 'Medium', 'High']},
    color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white",
    title="Average GPA by Study Category"
)
st.plotly_chart(fig1, use_container_width=True)
st.subheader("Interpretation")
st.write("Enter your interpretation here...")
st.markdown("---")

# 2. Social Media
st.header("2. Social Media Usage and Academic Performance")
fig2 = px.box(
    df, x='Social_Media_Hours_Daily', y='GPA_Midpoint', color='Social_Media_Hours_Daily',
    category_orders={'Social_Media_Hours_Daily': ['< 1 hours', '2 - 3 hours', '4 - 5 hours', '> 6 hours']},
    points='all', color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white",
    title="GPA Distribution by Social Media Usage"
)
st.plotly_chart(fig2, use_container_width=True)
st.subheader("Interpretation")
st.write("Enter your interpretation here...")
st.markdown("---")

# 3. Health Issues
st.header("3. Health Issues and Academic Outcomes")
health_gpa = df.groupby('Health_Issues_Text')['GPA_Midpoint'].mean().reset_index()
fig3 = px.bar(
    health_gpa, x='Health_Issues_Text', y='GPA_Midpoint', color='Health_Issues_Text',
    category_orders={'Health_Issues_Text': ['No', 'Yes']},
    color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white",
    title="Average GPA by Health Issues"
)
st.plotly_chart(fig3, use_container_width=True)
st.subheader("Interpretation")
st.write("Enter your interpretation here...")
st.markdown("---")

# 4. Attendance
st.header("4. Attendance and Performance Trend")
attn_gpa = df.groupby('Attendance_Midpoint')['GPA_Midpoint'].mean().reset_index()
fig4 = px.line(
    attn_gpa, x='Attendance_Midpoint', y='GPA_Midpoint', 
    markers=True, template="simple_white",
    title="GPA Trend over Attendance Percentage"
)
fig4.update_traces(line_color='#AEC6CF', marker=dict(size=10, color='#FFB347'))
st.plotly_chart(fig4, use_container_width=True)
st.subheader("Interpretation")
st.write("Enter your interpretation here...")
st.markdown("---")

# 5. Correlation Heatmap
st.header("5. Correlation Heatmap")
num_cols = ['Study_Hours_Daily_Midpoint', 'Social_Media_Hours_Daily_Midpoint', 'Attendance_Midpoint', 'GPA_Midpoint']
corr = df[num_cols].corr()
fig5 = px.imshow(
    corr, text_auto=".2f", aspect="auto",
    color_continuous_scale='RdBu_r', 
    title='Statistical Correlation of Key Factors'
)
fig5.update_layout(template="simple_white")
st.plotly_chart(fig5, use_container_width=True)
st.subheader("Interpretation")
st.write("Enter your interpretation here...")
