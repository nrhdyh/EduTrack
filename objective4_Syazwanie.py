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

# 2. EXACT strings and order from your dataset
cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']

# 3. Create the cross-tabulation and convert to percentages
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])
available_order = [c for c in cgpa_order if c in cross_tab.columns]
cross_tab = cross_tab[available_order]
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100

# 4. Transform to Long Format (Required for Plotly Express)
# We reset the index so 'Skills_Category' becomes a column, then melt.
df_plot = percentage_dist.reset_index().melt(
    id_vars='Skills_Category', 
    var_name='CGPA Range', 
    value_name='Percentage'
)

# 5. Create the Plotly Figure
fig = px.bar(
    df_plot,
    y='Skills_Category',
    x='Percentage',
    color='CGPA Range',
    orientation='h',
    title='Percentage Distribution of CGPA Ranges by Skill Category',
    # Match the colors from your image exactly
    color_discrete_map={
        '2.50 – 2.99': '#e74c3c', # Red
        '3.00 – 3.69': '#f1c40f', # Yellow
        '3.70 - 4.00': '#2ecc71'  # Green
    },
    category_orders={
        'CGPA Range': cgpa_order,
        # This keeps the Y-axis in the same order as your dataframe index
        'Skills_Category': percentage_dist.index.tolist() 
    },
    # This creates the text labels inside the bars
    text=df_plot['Percentage'].apply(lambda x: f'{x:.1f}%' if x > 0 else '')
)

# 6. Fine-tune styling to match the Matplotlib output
fig.update_layout(
    xaxis_title='Percentage of Students (%)',
    yaxis_title='Skills Category',
    xaxis_range=[0, 100],
    legend_title_text='CGPA Range',
    # White background to match the "clean" look
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title_font=dict(size=18),
    # Adjust margins to ensure labels aren't cut off
    margin=dict(l=150, r=20, t=80, b=50),
    # Legend positioning (similar to bbox_to_anchor in matplotlib)
    legend=dict(
        bordercolor="lightgrey",
        borderwidth=1
    )
)

# Bold black text for the labels inside the bars
fig.update_traces(
    textposition='inside',
    textfont=dict(color='black', family='Arial Black')
)

# Add vertical gridlines for the percentages (optional, matches the clean look)
fig.update_xaxes(showgrid=True, gridcolor='lightgrey')

# 7. Display in Streamlit
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
