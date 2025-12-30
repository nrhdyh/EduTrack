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

# 2. Get the unique CGPA values actually present in your data
# This avoids the "dash" character mismatch issue entirely
actual_labels = df['CGPA'].unique().tolist()

# 3. Sort them so they appear in academic order (Low to High)
# This sorts them based on the first two numbers (e.g., 2.50, 3.00, 3.70)
actual_labels.sort()

# 4. Create the cross-tabulation using the actual labels found
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])
cross_tab = cross_tab[actual_labels]

# 5. Convert to percentages
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100

# 6. Transform for Plotly
df_plot = percentage_dist.reset_index().melt(
    id_vars='Skills_Category', 
    var_name='CGPA Range', 
    value_name='Percentage'
)

# 7. Create Plotly Figure with a flexible color map
# This maps colors based on the position in your sorted list 
# (Red for lowest, Yellow for middle, Green for highest)
colors = ['#e74c3c', '#f1c40f', '#2ecc71']
color_map = {label: colors[i] for i, label in enumerate(actual_labels)}

fig = px.bar(
    df_plot,
    y='Skills_Category',
    x='Percentage',
    color='CGPA Range',
    orientation='h',
    title='Percentage Distribution of CGPA Ranges by Skill Category',
    color_discrete_map=color_map,
    category_orders={'CGPA Range': actual_labels},
    text=df_plot['Percentage'].apply(lambda x: f'{x:.1f}%' if x > 0 else '')
)

fig.update_layout(
    xaxis_range=[0, 100],
    plot_bgcolor='white',
    legend_title_text='CGPA Range'
)

fig.update_traces(textposition='inside', textfont=dict(color='black', family='Arial Black'))

st.plotly_chart(fig, use_container_width=True)


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
