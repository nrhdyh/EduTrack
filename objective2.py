import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="EduTrack Student Dashboard", layout="centered")

# --- Data Loading & Helper Functions ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv'
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

# --- Data Processing ---
df_url = load_data()

# Calculate midpoints for metrics
df_url['Study_Hours_Daily_Midpoint'] = df_url['Study_Hours_Daily'].apply(calculate_hours_midpoint)
df_url['Social_Media_Hours_Daily_Midpoint'] = df_url['Social_Media_Hours_Daily'].apply(calculate_hours_midpoint)

# Compute Averages for the Summary
avg_gpa = df_url['GPA_Midpoint'].mean()
avg_study = df_url['Study_Hours_Daily_Midpoint'].mean()
avg_social = df_url['Social_Media_Hours_Daily_Midpoint'].mean()
avg_attendance = df_url['Attendance_Midpoint'].mean()

# --- App Header ---
st.title("🎓 Study and Lifestyle")
st.markdown("""Study habits, social media usage and health factors are aspects of lifestyle that could have influence the academic performance of UMK students.
However, the relationship between these factors and students' academic achievement is still poorly explored through visual analysis. Therefore, this study aims
to visualize and understand the realtionship between lifestyle factors and students' academic performance.""")
st.markdown("---")

# --- KEY METRICS SUMMARY (4 Columns) ---
st.subheader("📌 Key Summary Insights")
m1, m2, m3, m4 = st.columns(4)

m1.metric(label="Average GPA", value=f"{avg_gpa:.2f}")
m2.metric(label="Avg Study Hours", value=f"{avg_study:.1f} hrs")
m3.metric(label="Avg Social Media", value=f"{avg_social:.1f} hrs")
m4.metric(label="Avg Attendance", value=f"{avg_attendance:.1f}%")

st.markdown("---")

# --- Visualization 1: Study Hours ---
st.header("1. Impact of Study Habits")
study_gpa = df_url.groupby('Study_Hours_Category')['GPA_Midpoint'].mean().reset_index()
fig_study = px.bar(
    study_gpa, x='Study_Hours_Category', y='GPA_Midpoint', color='Study_Hours_Category',
    title='Average GPA by Study Category',
    category_orders={'Study_Hours_Category': ['Low', 'Medium', 'High']},
    color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white"
)
st.plotly_chart(fig_study, use_container_width=True)
st.subheader("Interpretation")
st.write("Interpretation text for study habits goes here...")
st.markdown("---")

# --- 7. Visualization 2: Social Media ---
st.header("2. Social Media Usage and Academic Spread")
fig_social = px.box(
    df_url, x='Social_Media_Hours_Daily', y='GPA_Midpoint', color='Social_Media_Hours_Daily',
    title='GPA Distribution by Social Media Usage',
    category_orders={'Social_Media_Hours_Daily': ['< 1 hours', '2 - 3 hours', '4 - 5 hours', '> 6 hours']},
    points='all', color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white"
)
st.plotly_chart(fig_social, use_container_width=True)
st.subheader("Interpretation")
st.write("Interpretation text for social media goes here...")
st.markdown("---")

# --- 8. Visualization 3: Health Issues ---
st.header("3. Health Factors and Academic Outcomes")
health_gpa = df_url.groupby('Health_Issues_Text')['GPA_Midpoint'].mean().reset_index()
fig_health = px.bar(
    health_gpa, x='Health_Issues_Text', y='GPA_Midpoint', color='Health_Issues_Text',
    title='Average GPA Midpoint by Health Issues',
    category_orders={'Health_Issues_Text': ['No', 'Yes']},
    color_discrete_sequence=px.colors.qualitative.Pastel, template="simple_white"
)
st.plotly_chart(fig_health, use_container_width=True)
st.subheader("Interpretation")
st.write("Interpretation text for health factors goes here...")
st.markdown("---")

# --- 9. Visualization 4: Attendance Trend ---
st.header("4. Attendance and Performance Trend")
attendance_gpa_line = df_url.groupby('Attendance_Midpoint')['GPA_Midpoint'].mean().reset_index()
fig_line = px.line(
    attendance_gpa_line, x='Attendance_Midpoint', y='GPA_Midpoint',
    title='Average GPA Midpoint vs. Attendance Midpoint', markers=True, template="simple_white"
)
fig_line.update_traces(line_color='#AEC6CF', marker=dict(size=10, color='#FFB347'), name="GPA Trend", showlegend=True)
st.plotly_chart(fig_line, use_container_width=True)
st.subheader("Interpretation")
st.write("Interpretation text for attendance trend goes here...")
st.markdown("---")

# --- 10. Visualization 5: Correlation Heatmap ---
st.header("5. Correlation Analysis")
numerical_cols = ['Study_Hours_Daily_Midpoint', 'Social_Media_Hours_Daily_Midpoint', 'Attendance_Midpoint', 'GPA_Midpoint']
correlation_matrix = df_url[numerical_cols].corr()

fig_heat = px.imshow(
    correlation_matrix, text_auto=".2f", aspect="auto",
    title='Correlation Heatmap of Study habits and Academic Performance',
    color_continuous_scale=px.colors.diverging.PiYG, 
    labels=dict(color="Correlation")
)
fig_heat.update_layout(template="simple_white")
st.plotly_chart(fig_heat, use_container_width=True)

st.subheader("Interpretation")
st.write("Summarize the overall statistical relationships found in the heatmap above...")
