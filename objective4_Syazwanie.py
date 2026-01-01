import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
df = pd.read_csv(url)

df = load_data()

st.title("Student Performance Dashboard")

# --- 1. PERFORMANCE DENSITY (KDE Replacement) ---
st.header("Performance Density: Active vs Non-Active")

# Plotly Express doesn't have a direct KDE, so we use Figure Factory or Histogram with marginals
# Using crest-like colors (Teals/Blues)
fig1 = px.histogram(
    df, 
    x='CGPA_Midpoint', 
    color='Co_Curriculum_Activities_Text',
    marginal="violin", # Adds a violin plot on top
    nbins=30,
    histnorm='probability density',
    barmode='overlay',
    color_discrete_sequence=px.colors.sequential.Crest,
    title='Performance Density : Active vs Non-Active students'
)
st.plotly_chart(fig1, use_container_width=True)


# --- 2. AVERAGE CGPA BY SKILL DEVELOPMENT ---
st.header("Skill Development & Co-Curricular Participation")

df_grouped = df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    df_grouped,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    barmode='group',
    title='Average CGPA by Skill Development and Co-Curricular Participation',
    labels={
        'Skill_Development_Hours_Category': 'Skill Development Hours',
        'CGPA_Midpoint': 'Average CGPA',
        'Co_Curriculum_Activities_Text': 'Co-Curricular Participation'
    }
)
st.plotly_chart(fig2, use_container_width=True)


# --- 3. PERCENTAGE DISTRIBUTION (Stacked Horizontal Bar) ---
st.header("CGPA Distribution by Skill Category")

cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])
available_order = [c for c in cgpa_order if c in cross_tab.columns]
cross_tab = cross_tab[available_order]

# Convert to percentages for Plotly
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0).reset_index()
# Melt the dataframe for Plotly Express
df_melted = percentage_dist.melt(id_vars='Skills_Category', var_name='CGPA Range', value_name='Percentage')
df_melted['Percentage'] *= 100

fig3 = px.bar(
    df_melted,
    y='Skills_Category',
    x='Percentage',
    color='CGPA Range',
    orientation='h',
    title='Percentage Distribution of CGPA Ranges by Skill Category',
    # Using your exact colors: Red, Yellow, Green
    color_discrete_map={
        available_order[0]: '#e74c3c', 
        available_order[1]: '#f1c40f', 
        available_order[2]: '#2ecc71'
    },
    text_auto='.1f' # Adds the percentage labels automatically
)
fig3.update_layout(xaxis_title="Percentage of Students (%)", yaxis_title="Skills Category")
st.plotly_chart(fig3, use_container_width=True)


# --- 4. VIOLIN PLOT ---
st.header("CGPA Density: Skill Dev vs Participation")

fig4 = px.violin(
    df,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    box=True,      # Similar to 'inner="quart"'
    points=None,   # Clean look
    color_discrete_sequence=px.colors.qualitative.Muted,
    title='CGPA Density: Skill Development Levels vs. Co-curricular Participation'
)

# Adding the horizontal mean line
overall_mean = df['CGPA_Midpoint'].mean()
fig4.add_hline(y=overall_mean, line_dash="dash", line_color="red", annotation_text="Overall Average")

st.plotly_chart(fig4, use_container_width=True)


# --- 5. LINE PLOT: ACADEMIC PROGRESSION ---
st.header("Academic Progression Trends")

# Calculating mean per group for the line plot
df_line = df.groupby(['Year_of_Study', 'Skill_Development_Hours_Category'])['CGPA_Midpoint'].mean().reset_index()

fig5 = px.line(
    df_line,
    x='Year_of_Study',
    y='CGPA_Midpoint',
    color='Skill_Development_Hours_Category',
    markers=True,
    title='Academic Progression: CGPA Trends by Year of Study & Skill Dev Level'
)
fig5.update_layout(xaxis_title='Year of Study', yaxis_title='CGPA Midpoint')
st.plotly_chart(fig5, use_container_width=True)
