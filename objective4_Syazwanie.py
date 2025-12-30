import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Page configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("🎓 Student Performance & Skill Development Analytics")

# 1. Load Data
# ---------------------------------------
# DATA LOADING (Fixes the NameError)
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

# --- VISUALIZATION 1: Performance Density (KDE Equivalent) ---
st.header("1. Performance Density")
# Plotly Express doesn't have a direct KDE, so we use Figure Factory's Distplot
# We split the data by the hue category
categories = df['Co_Curriculum_Activities_Text'].unique()
hist_data = [df[df['Co_Curriculum_Activities_Text'] == cat]['CGPA_Midpoint'].dropna() for cat in categories]
group_labels = [str(cat) for cat in categories]

fig1 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)
fig1.update_layout(title_text='Performance Density: Active vs Non-Active students', xaxis_title="CGPA Midpoint")
st.plotly_chart(fig1, use_container_width=True)


# --- VISUALIZATION 2: Average CGPA (Grouped Bar) ---
st.header("2. Average CGPA by Activity & Skills")
df_grouped = df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    df_grouped,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    barmode='group',
    title='Average CGPA by Skill Development and Co-Curricular Participation',
    labels={'CGPA_Midpoint': 'Avg CGPA', 'Skill_Development_Hours_Category': 'Skill Hours'},
    color_discrete_sequence=px.colors.qualitative.Prism
)
st.plotly_chart(fig2, use_container_width=True)


# --- VISUALIZATION 3: Percentage Distribution (Stacked Horizontal Bar) ---
st.header("3. CGPA Distribution by Skill Category")

# Re-applying your specific ordering logic
cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])
available_order = [c for c in cgpa_order if c in cross_tab.columns]
cross_tab = cross_tab[available_order]

# Convert to long format for Plotly Express
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage_dist = percentage_dist.reset_index().melt(id_vars='Skills_Category', var_name='CGPA_Range', value_name='Percentage')

fig3 = px.bar(
    percentage_dist,
    y='Skills_Category',
    x='Percentage',
    color='CGPA_Range',
    orientation='h',
    title='Percentage Distribution of CGPA Ranges by Skill Category',
    text=percentage_dist['Percentage'].apply(lambda x: f'{x:.1f}%'),
    color_discrete_map={'2.50 – 2.99': '#e74c3c', '3.00 – 3.69': '#f1c40f', '3.70 - 4.00': '#2ecc71'}
)
fig3.update_layout(xaxis_title="Percentage of Students (%)", yaxis_title="Skills Category")
st.plotly_chart(fig3, use_container_width=True)


# --- VISUALIZATION 4: Academic Progression (Line Plot) ---
st.header("4. Academic Progression Trends")

# Plotly's line chart automatically handles the grouping by 'hue' using the color parameter
fig4 = px.line(
    df, 
    x='Year_of_Study', 
    y='CGPA_Midpoint', 
    color='Skill_Development_Hours_Category',
    markers=True,
    title='Academic Progression: CGPA Trends by Year of Study & Skill Dev Level',
    # Plotly's line chart calculates the mean automatically if multiple points exist for one X
    category_orders={"Year_of_Study": sorted(df['Year_of_Study'].unique())} 
)
fig4.update_layout(yaxis_title="CGPA Midpoint", xaxis_gridcolor='rgba(0,0,0,0.1)', yaxis_gridcolor='rgba(0,0,0,0.1)')
st.plotly_chart(fig4, use_container_width=True)
