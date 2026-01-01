import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("Student Performance Analysis")

# ---------------------------------------
# 1. Performance Density (KDE Equivalent)
# ---------------------------------------
st.subheader("Performance Density: Active vs Non-Active Students")

# Plotly uses histograms with marginal violins to represent density/distribution
fig1 = px.histogram(
    df, 
    x='CGPA_Midpoint', 
    color='Co_Curriculum_Activities_Text',
    marginal="violin", 
    histnorm='probability density',
    barmode='overlay',
    color_discrete_sequence=px.colors.sequential.Crest,
    title='Performance Density : Active vs Non-Active students'
)
st.plotly_chart(fig1, use_container_width=True)


# ---------------------------------------
# 2. Average CGPA Grouped Bar Chart
# ---------------------------------------
st.subheader("Average CGPA by Skill Dev & Co-Curriculars")

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


# ---------------------------------------
# 3. Stacked Horizontal Percentage Bar
# ---------------------------------------
st.subheader("Percentage Distribution of CGPA by Skill Category")

# Reordering logic
cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])
available_order = [c for c in cgpa_order if c in cross_tab.columns]
cross_tab = cross_tab[available_order]

# Convert to percentage
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage_dist = percentage_dist.reset_index().melt(id_vars='Skills_Category', var_name='CGPA Range', value_name='Percentage')

fig3 = px.bar(
    percentage_dist,
    y='Skills_Category',
    x='Percentage',
    color='CGPA Range',
    orientation='h',
    text_auto='.1f',
    title='Percentage Distribution of CGPA Ranges by Skill Category',
    color_discrete_map={
        available_order[0]: '#e74c3c', 
        available_order[1]: '#f1c40f', 
        available_order[2]: '#2ecc71'
    }
)
fig3.update_layout(xaxis_title="Percentage (%)", yaxis_title="Skills Category")
st.plotly_chart(fig3, use_container_width=True)


# ---------------------------------------
# 4. Violin Plot
# ---------------------------------------
st.subheader("CGPA Density: Skills vs Co-Curricular")

fig4 = px.violin(
    df,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    box=True,
    points=None,
    color_discrete_sequence=px.colors.qualitative.Muted,
    title='CGPA Density: Skill Development Levels vs. Co-curricular Participation'
)

# Add horizontal baseline for average
overall_avg = df['CGPA_Midpoint'].mean()
fig4.add_hline(y=overall_avg, line_dash="dash", line_color="red", annotation_text="Overall Avg")

st.plotly_chart(fig4, use_container_width=True)


# ---------------------------------------
# 5. Line Plot: Academic Progression
# ---------------------------------------
st.subheader("Academic Progression Trends")

# Calculate means for the line
df_line = df.groupby(['Year_of_Study', 'Skill_Development_Hours_Category'])['CGPA_Midpoint'].mean().reset_index()

fig5 = px.line(
    df_line,
    x='Year_of_Study',
    y='CGPA_Midpoint',
    color='Skill_Development_Hours_Category',
    markers=True,
    title='Academic Progression: CGPA Trends by Year of Study & Skill Dev Level'
)
st.plotly_chart(fig5, use_container_width=True)
