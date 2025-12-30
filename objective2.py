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

# Calculate midpoints for correlation and metrics
df['Study_Hours_Daily_Midpoint'] = df['Study_Hours_Daily'].apply(calculate_hours_midpoint)
df['Social_Media_Hours_Daily_Midpoint'] = df['Social_Media_Hours_Daily'].apply(calculate_hours_midpoint)

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title("🎓 Study and Lifestyle")
st.markdown("""
Study habits, social media usage and health factors are aspects of lifestyle that could have influence the academic performance of UMK students.
However, the relationship between these factors and students' academic is still poorly explored through visual analysis. Therefore, this study
aims to visualize and understand the relationship between lifestyle factors and students' academic performance.
""")
st.markdown("---")

# =====================================================
# 📊 SUMMARY INSIGHT BLOCK BOXES
# =====================================================
st.subheader("📊 Key Academic Summary")

# Filters (Row style)
#col_f1, col_f2, col_f3 = st.columns(3)

#with col_f1:
    #selected_gender = st.selectbox("Filter by Gender", ["All"] + sorted(df["Gender"].dropna().unique().tolist()))

#with col_f2:
    #selected_faculty = st.selectbox("Filter by Faculty", ["All"] + sorted(df["Faculty_Short"].dropna().unique().tolist()))

#with col_f3:
    #selected_living = st.selectbox("Filter by Living Arrangement", ["All"] + sorted(df["Living_With"].dropna().unique().tolist()))

# Apply filters
#f_df = df.copy()
#if selected_gender != "All":
    #f_df = f_df[f_df["Gender"] == selected_gender]
#if selected_faculty != "All":
    #f_df = f_df[f_df["Faculty_Short"] == selected_faculty]
#if selected_living != "All":
    #f_df = f_df[f_df["Living_With"] == selected_living]

# Compute Metrics
avg_gpa = f_df["GPA_Midpoint"].mean() if not f_df.empty else 0
avg_study = f_df["Study_Hours_Daily_Midpoint"].mean() if not f_df.empty else 0
avg_social = f_df["Social_Media_Hours_Daily_Midpoint"].mean() if not f_df.empty else 0
avg_attendance = f_df["Attendance_Midpoint"].mean() if not f_df.empty else 0

# Block Style (Matching your Demographic page)
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
# 📈 VISUALIZATIONS (ONE BY ONE)
# =====================================================

# 1. Study Hours
st.header("1. Average GPA by Study Hours")
study_gpa = f_df.groupby('Study_Hours_Category')['GPA_Midpoint'].mean().reset_index()
fig1 = px.bar(
    study_gpa, x='Study_Hours_Category', y='GPA_Midpoint', color='Study_Hours_Category',
    category_orders={'Study_Hours_Category': ['Low', 'Medium', 'High']},
    color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white"
)
st.plotly_chart(fig1, use_container_width=True)
st.info("**Interpretation:** Higher study hour categories generally correlate with higher GPA midpoints.")

# 2. Social Media
st.header("2. Social Media Usage and Academic Performance")
fig2 = px.box(
    f_df, x='Social_Media_Hours_Daily', y='GPA_Midpoint', color='Social_Media_Hours_Daily',
    category_orders={'Social_Media_Hours_Daily': ['< 1 hours', '2 - 3 hours', '4 - 5 hours', '> 6 hours']},
    points='all', color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white"
)
st.plotly_chart(fig2, use_container_width=True)
st.info("**Interpretation:** This distribution highlights how excessive social media use might impact the range of student performance.")

# 3. Health Issues
st.header("3. Health Issues and Academic Outcomes")
health_gpa = f_df.groupby('Health_Issues_Text')['GPA_Midpoint'].mean().reset_index()
fig3 = px.bar(
    health_gpa, x='Health_Issues_Text', y='GPA_Midpoint', color='Health_Issues_Text',
    category_orders={'Health_Issues_Text': ['No', 'Yes']},
    color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white"
)
st.plotly_chart(fig3, use_container_width=True)
st.info("**Interpretation:** Comparison of GPA averages between students with and without reported health issues.")

# 4. Attendance
st.header("4. Attendance and Performance Trend")
attn_gpa = f_df.groupby('Attendance_Midpoint')['GPA_Midpoint'].mean().reset_index()
fig4 = px.line(attn_gpa, x='Attendance_Midpoint', y='GPA_Midpoint', markers=True, template="simple_white")
fig4.update_traces(line_color='#AEC6CF', marker=dict(size=10, color='#FFB347'))
st.plotly_chart(fig4, use_container_width=True)
st.info("**Interpretation:** The trend line shows the relationship between class attendance percentages and GPA.")

# 5. Heatmap
st.header("5. Correlation Heatmap")
num_cols = ['Study_Hours_Daily_Midpoint', 'Social_Media_Hours_Daily_Midpoint', 'Attendance_Midpoint', 'GPA_Midpoint']
if not f_df.empty and len(f_df) > 1:
    corr = f_df[num_cols].corr()
    fig5 = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale='RdBu_r',
        title='Correlation Heatmap'
    )
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.warning("Not enough data to display correlation for the selected filters.")

st.info("**Interpretation:** Red indicates a strong positive relationship, while Blue indicates a negative relationship.")
