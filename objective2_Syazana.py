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

# ---------------------------------------
# LOAD & PRE-PROCESS DATA
# ---------------------------------------
df = load_data()
df['Study_Hours_Daily_Midpoint'] = df['Study_Hours_Daily'].apply(calculate_hours_midpoint)
df['Social_Media_Hours_Daily_Midpoint'] = df['Social_Media_Hours_Daily'].apply(calculate_hours_midpoint)

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title("🎓 Relationship between Study Habits, Social Media Usage and Health Factors in influencing Academic Performance of UMK Students.")
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
"""

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div style="{block_style}"><h4>🏆 Average GPA</h4><p style="font-size:22px; font-weight:bold;">{avg_gpa:.2f}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{block_style}"><h4>✍️ Avg Study Hours Daily</h4><p style="font-size:22px; font-weight:bold;">{avg_study:.1f} hrs</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{block_style}"><h4>🤳 Avg Social Media Daily</h4><p style="font-size:22px; font-weight:bold;">{avg_social:.1f} hrs</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{block_style}"><h4>🎒 Avg Attendance</h4><p style="font-size:22px; font-weight:bold;">{avg_attendance:.1f}%</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 📈 VISUALIZATION 1: STUDY HOURS
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
    The graph above shows the relationship between the study hours and academic performance of UMK students.
    - The findings show that the average GPA increases with the increase in study hours category, where 
    students who spend more time studying record a better academic performance.
    - This pattern suggests that consistent study habits are one of the lifestyle factors that are 
    related to students' academic achievement.
    - Overall, this show that study habits are related to the academic performance of UMK students.
    """)

st.markdown("---")

# =====================================================
# 📈 VISUALIZATION 2: SOCIAL MEDIA
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
    The boxplot above illustrates the distribution of GPA based on daily social media usage categories.
    - The findings shows that the median GPA for most categories was nearly identical, but students with 
    higher social media usage showed greater variation in academic performance.
    - This suggests that social media usage as part of UMK students' lifestyle has the potential to influence
    the stability and consistency of academic performance.
    """)

st.markdown("---")

# =====================================================
# 📈 VISUALIZATION 3: HEALTH ISSUES
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
    The bar chart above compares the average GPAs between students with health issues and students who did not
    have any health problems.
    - This finding shows that students without health issues recorded a higher average GPAs than students with health issues.
    - This suggest that health conditions can affect students' ability to maintain focus and effective study routines.
    - Overall, this finding supports that health factors are related to academic performance.
    """)

st.markdown("---")

# =====================================================
# 📈 VISUALIZATION 4: ATTENDANCE TREND
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
    The graph above shows the overall of attendance and academic performance.
    - The finding presents in general that increased attendance rate are associated with improves student
    academic performance.
    - However, students in the moderate attendance category recorded slightly lower average GPAs than the low
    and high attendance categories.
    - Overall, this pattern suggests that the relationship between attendance and academic performance is 
    not completely linear.
    """)

st.markdown("---")

# =====================================================
# 📈 VISUALIZATION 5: CORRELATION HEATMAP
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
    The correlation heatmap above illustrates a comprehensive overview of the relationship between lifestyle factors
    and academic performance of UMK students.
    - The finding shows that daily study hours and attendance showed a significant positive correlation with GPA, while
    social media use showed a weaker correlation with GPA.
    - Overall, this suggests that academic performance can be influenced by a combination of several lifestyle factors.
    """)
