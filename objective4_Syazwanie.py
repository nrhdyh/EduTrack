import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# DATA LOADING (Fixes the NameError)
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

# --- CHART 1: Grouped Bar Chart ---
# Average CGPA by Skill Development and Co-Curricular Participation
df_grouped = df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()

fig1 = px.bar(
    df_grouped,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    barmode='group',
    title='Average CGPA by Skill Development & Co-Curricular Participation',
    labels={'CGPA_Midpoint': 'Avg CGPA', 'Skill_Development_Hours_Category': 'Skill Dev Hours'},
    category_orders={"Skill_Development_Hours_Category": ["Low", "Medium", "High"]}
)
st.plotly_chart(fig1, use_container_width=True)


# --- CHART 2: Stacked Horizontal Bar ---

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

# --- CHART 3: Ranking Bar Chart ---
# Average CGPA by Skill Focus
skill_rank = df.groupby('Skills_Category')['CGPA_Midpoint'].mean().sort_values(ascending=True).reset_index()

fig3 = px.bar(
    skill_rank,
    x='CGPA_Midpoint',
    y='Skills_Category',
    orientation='h',
    title='Ranking: Average CGPA by Skill Focus',
    color='CGPA_Midpoint',
    color_continuous_scale='Magma'
)
fig3.update_layout(xaxis_title="Mean CGPA", yaxis_title="Skill Category", xaxis_range=[0, 4])
st.plotly_chart(fig3, use_container_width=True)


# --- CHART 4: Heatmap ---
# Average CGPA by Skill Dev Hours and Co-Curricular Participation
heatmap_data = df.pivot_table(
    values='CGPA_Midpoint',
    index='Skill_Development_Hours_Category',
    columns='Co_Curriculum_Activities_Text',
    aggfunc='mean'
).reindex(['Low', 'Medium', 'High'])

fig4 = px.imshow(
    heatmap_data,
    labels=dict(x="Co-Curricular Participation", y="Skill Dev Hours", color="Avg CGPA"),
    text_auto='.2f',
    aspect="auto",
    color_continuous_scale='Viridis',
    title='Heatmap: Avg CGPA by Skill Dev and Co-Curriculars'
)
st.plotly_chart(fig4, use_container_width=True)


# --- CHART 5: Line Plot ---
# Academic Progression: CGPA Trends by Year of Study
# We first aggregate to replicate sns.lineplot(errorbar=None)
df_line = df.groupby(['Year_of_Study', 'Skill_Development_Hours_Category'])['CGPA_Midpoint'].mean().reset_index()

fig5 = px.line(
    df_line,
    x='Year_of_Study',
    y='CGPA_Midpoint',
    color='Skill_Development_Hours_Category',
    markers=True,
    title='Academic Progression: CGPA Trends by Year & Skill Dev Level',
    category_orders={"Skill_Development_Hours_Category": ["Low", "Medium", "High"]}
)
fig5.update_layout(yaxis_title="Mean CGPA", xaxis_title="Year of Study")
st.plotly_chart(fig5, use_container_width=True)
