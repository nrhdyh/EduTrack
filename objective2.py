import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="EduTrack Dashboard", layout="wide")

# --- Data Loading (Cached) ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv'
    df = pd.read_csv(url)
    return df

df_url = load_data()

# --- App Header ---
st.title("🎓 Student Performance Analytics")
st.markdown("Exploring the relationship between study habits and academic results.")

# --- Data Preview Section ---
with st.expander("🔍 View Raw Data Preview"):
    st.dataframe(df_url.head(), use_container_width=True)

# --- Visualization Logic ---
# Grouping data
study_gpa = df_url.groupby('Study_Hours_Category')['GPA_Midpoint'].mean().reset_index()
category_order = ['Low', 'Medium', 'High']

# Creating the Pastel Bar Chart
fig = px.bar(
    study_gpa,
    x='Study_Hours_Category',
    y='GPA_Midpoint',
    color='Study_Hours_Category',
    title='Average GPA Midpoint by Study Hours Category',
    labels={
        'Study_Hours_Category': 'Study Hours Category',
        'GPA_Midpoint': 'Average GPA'
    },
    category_orders={'Study_Hours_Category': category_order},
    color_discrete_sequence=px.colors.qualitative.Pastel,
    template="simple_white"  # This ensures a clean, neat background
)

# Polishing the Layout
fig.update_layout(
    xaxis_title="Study Hours Category",
    yaxis_title="Average GPA",
    legend_title="Category",
    showlegend=True,
    hovermode="x unified"
)

# --- Displaying the Chart ---
st.plotly_chart(fig, use_container_width=True)

# --- Insights (Optional) ---
st.info("The chart above shows how different levels of study hours impact the average GPA midpoint.")
