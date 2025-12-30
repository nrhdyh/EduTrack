import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(page_title="Academic Performance", layout="wide")

# ---------------------------------------
# HELPER FUNCTIONS & DATA
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
        elif '>' in cleaned_range: return float(cleaned_range.replace('>', '')) + 0.5
        elif '<' in cleaned_range: return float(cleaned_range.replace('<', '')) - 0.5
    return np.nan

df = load_data()
df['Study_Hours_Daily_Midpoint'] = df['Study_Hours_Daily'].apply(calculate_hours_midpoint)
df['Social_Media_Hours_Daily_Midpoint'] = df['Social_Media_Hours_Daily'].apply(calculate_hours_midpoint)

# ---------------------------------------
# STYLING & SUMMARY METRICS
# ---------------------------------------
block_style = """
    background: linear-gradient(135deg, #5E35B1, #3949AB);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
"""

st.title("🎓 Relationship between Study Habits, Social Media Usage and Health Factors in influencing Academic Performance of UMK Students.")
st.markdown("""
Study habits, social media usage and health factors are aspects of lifestyle that could have influence the academic performance of UMK students.
However, the relationship between these factors and students' academic is still poorly explored through visual analysis. Therefore, this study
aims to visualize and understand the relationship between lifestyle factors and students' academic performance.
""")
st.markdown("---")

# Summary Metrics Row
avg_gpa = df["GPA_Midpoint"].mean()
avg_study = df["Study_Hours_Daily_Midpoint"].mean()
avg_social = df["Social_Media_Hours_Daily_Midpoint"].mean()
avg_attendance = df["Attendance_Midpoint"].mean()

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
for col, label, val, unit in zip([col_m1, col_m2, col_m3, col_m4], 
                                  ["Average GPA", "Avg Study Hours", "Avg Social Media", "Avg Attendance"],
                                  [avg_gpa, avg_study, avg_social, avg_attendance],
                                  ["", " hrs", " hrs", "%"]):
    col.markdown(f'<div style="{block_style}"><h3>{label}</h3><p style="font-size:20px; font-weight:bold;">{val:.2f}{unit}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# VISUALIZATION 1: STUDY HOURS
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Bar Chart: Average GPA by Study Hours</h3></div>', unsafe_allow_html=True)

study_gpa = df.groupby('Study_Hours_Category')['GPA_Midpoint'].mean().reset_index()
fig1 = px.bar(study_gpa, x='Study_Hours_Category', y='GPA_Midpoint', color='Study_Hours_Category',
             category_orders={'Study_Hours_Category': ['Low', 'Medium', 'High']},
             color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 📈 Average GPA by Study Hours")
show_desc1 = st.checkbox("Show Interpretation", value=True, key="desc1")
if show_desc1:
    st.markdown("""
    Interpretation.
    """)

st.markdown("<br><br>---", unsafe_allow_html=True)

# =====================================================
# VISUALIZATION 2: SOCIAL MEDIA
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Box Plot: Social Media Usage and Acedemic Performance</h3></div>', unsafe_allow_html=True)

fig2 = px.box(df, x='Social_Media_Hours_Daily', y='GPA_Midpoint', color='Social_Media_Hours_Daily',
             category_orders={'Social_Media_Hours_Daily': ['< 1 hours', '2 - 3 hours', '4 - 5 hours', '> 6 hours']},
             points='all', color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📈 Social Media vs Academic Performance")
show_desc2 = st.checkbox("Show Interpretation", value=True, key="desc2")
if show_desc2:
    st.markdown("""
    Interpretation
    """)

st.markdown("<br><br>---", unsafe_allow_html=True)

# =====================================================
# VISUALIZATION 3: HEALTH ISSUES
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ Bar Chart: Health Issues and Academic Outcomes</h3></div>', unsafe_allow_html=True)

health_gpa = df.groupby('Health_Issues_Text')['GPA_Midpoint'].mean().reset_index()
fig3 = px.bar(health_gpa, x='Health_Issues_Text', y='GPA_Midpoint', color='Health_Issues_Text',
             category_orders={'Health_Issues_Text': ['No', 'Yes']},
             color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 📈 Health Issues vs Average GPA")
show_desc3 = st.checkbox("Show Interpretation", value=True, key="desc3")
if show_desc3:
    st.markdown("""
    Interpretation.
    """)

st.markdown("<br><br>---", unsafe_allow_html=True)

# =====================================================
# VISUALIZATION 4: ATTENDANCE TREND
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Line Plot: Attendance and Performance Trend</h3></div>', unsafe_allow_html=True)

attn_gpa = df.groupby('Attendance_Midpoint')['GPA_Midpoint'].mean().reset_index()
fig4 = px.line(attn_gpa, x='Attendance_Midpoint', y='GPA_Midpoint', markers=True, template="simple_white")
fig4.update_traces(line_color='#AEC6CF', marker=dict(size=10, color='#FFB347'))
st.plotly_chart(fig4, use_container_width=True)

st.markdown("### 📈 Attendance vs Academic Performance")
show_desc4 = st.checkbox("Show Interpretation", value=True, key="desc4")
if show_desc4:
    st.markdown("""
    Interpretation.
    """)

st.markdown("<br><br>---", unsafe_allow_html=True)

# =====================================================
# VISUALIZATION 5: CORRELATION HEATMAP
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ Correlation Heatmap</h3></div>', unsafe_allow_html=True)

num_cols = ['Study_Hours_Daily_Midpoint', 'Social_Media_Hours_Daily_Midpoint', 'Attendance_Midpoint', 'GPA_Midpoint']
corr = df[num_cols].corr()
fig5 = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', template="simple_white")
st.plotly_chart(fig5, use_container_width=True)

st.markdown("### 📈 Correlation Heatmap")
show_desc5 = st.checkbox("Show Interpretation", value=True, key="desc5")
if show_desc5:
    st.markdown("""
    Interpretation.
    """)
