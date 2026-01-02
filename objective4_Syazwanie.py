import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Page configuration
st.set_page_config(page_title="EduTrack Performance Dashboard", layout="wide")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance_ver2.csv"
    data = pd.read_csv(url)
    return data

df = load_data()

st.title("🎓 Student Performance & Skill Development Analytics")
st.markdown("---")

# Layout: Two columns for the first two charts
col1, col2 = st.columns(2)

with col1:
    ### 1. Performance Density (KDE Plot)
    st.subheader("Performance Density: Active vs Non-Active")
    
    # Filter out nulls for the distribution plot
    active = df[df['Co_Curriculum_Activities_Text'] == 'Yes']['CGPA_Midpoint'].dropna()
    inactive = df[df['Co_Curriculum_Activities_Text'] == 'No']['CGPA_Midpoint'].dropna()
    
    hist_data = [active, inactive]
    group_labels = ['Active Students', 'Non-Active Students']
    colors = ['#2b83ba', '#abdda4'] # Crest-like palette colors

    fig1 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False, colors=colors)
    fig1.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    ### 2. Average CGPA Grouped Bar
    st.subheader("Avg CGPA by Skill & Co-Curriculars")
    
    df_grouped = df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()

    fig2 = px.bar(
        df_grouped,
        x='Skill_Development_Hours_Category',
        y='CGPA_Midpoint',
        color='Co_Curriculum_Activities_Text',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

### 3. Percentage Distribution Stacked Bar
st.subheader("CGPA Range Distribution by Skill Category")

cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']
# Creating the cross-tabulation and converting to long-form for Plotly Express
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])
available_order = [c for c in cgpa_order if c in cross_tab.columns]
cross_tab = cross_tab[available_order]
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage_dist = percentage_dist.reset_index().melt(id_vars='Skills_Category', var_name='CGPA_Range', value_name='Percentage')

fig3 = px.bar(
    percentage_dist,
    y='Skills_Category',
    x='Percentage',
    color='CGPA_Range',
    orientation='h',
    color_discrete_map={'2.50 – 2.99': '#e74c3c', '3.00 – 3.69': '#f1c40f', '3.70 - 4.00': '#2ecc71'},
    text=percentage_dist['Percentage'].apply(lambda x: f'{x:.1f}%')
)
fig3.update_layout(xaxis_title="Percentage of Students (%)", yaxis_title="Skills Category", height=500)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Layout: Two columns for the final two charts
col3, col4 = st.columns(2)

with col3:
    ### 4. Split Violin Plot
    st.subheader("CGPA Density: Skill vs Co-curricular")
    
    fig4 = go.Figure()

    # Manual creation of "Split" violin
    fig4.add_trace(go.Violin(
        x=df['Skill_Development_Hours_Category'][df['Co_Curriculum_Activities_Text'] == 'Yes'],
        y=df['CGPA_Midpoint'][df['Co_Curriculum_Activities_Text'] == 'Yes'],
        legendgroup='Yes', name='Active', side='positive', line_color='#1f77b4', meanline_visible=True
    ))
    fig4.add_trace(go.Violin(
        x=df['Skill_Development_Hours_Category'][df['Co_Curriculum_Activities_Text'] == 'No'],
        y=df['CGPA_Midpoint'][df['Co_Curriculum_Activities_Text'] == 'No'],
        legendgroup='No', name='Non-Active', side='negative', line_color='#ff7f0e', meanline_visible=True
    ))
    
    # Baseline mean line
    fig4.add_hline(y=df['CGPA_Midpoint'].mean(), line_dash="dash", line_color="red")
    fig4.update_layout(violinmode='overlay', height=450)
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    ### 5. Academic Progression Line Chart
    st.subheader("CGPA Progression by Year")
    
    # Aggregating for line chart
    df_line = df.groupby(['Year_of_Study', 'Skill_Development_Hours_Category'])['CGPA_Midpoint'].mean().reset_index()
    
    fig5 = px.line(
        df_line, 
        x='Year_of_Study', 
        y='CGPA_Midpoint', 
        color='Skill_Development_Hours_Category',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig5.update_layout(yaxis_title="Mean CGPA Midpoint", height=450)
    st.plotly_chart(fig5, use_container_width=True)


# --- HEATMAP: Skill Dev vs Co-Curricular ---
st.header("Average CGPA Heatmap")

# 1. Create the pivot table (same logic as your Seaborn code)
heatmap_data = df.pivot_table(
    values='CGPA_Midpoint',
    index='Skill_Development_Hours_Category',
    columns='Co_Curriculum_Activities_Text',
    aggfunc='mean'
)

# 2. Ensure logical ordering for the rows
hour_order = ['Low', 'Medium', 'High']
# intersection used to avoid errors if a category is missing in the data
available_order = [h for h in hour_order if h in heatmap_data.index]
heatmap_data = heatmap_data.reindex(index=available_order)

# 3. Create the Plotly Heatmap
fig_heatmap = px.imshow(
    heatmap_data,
    labels=dict(x="Co-Curricular Participation", y="Skill Development Hours", color="Avg CGPA"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    text_auto='.2f',          # Equivalent to annot=True and fmt='.2f'
    color_continuous_scale='Viridis', # Matches your cmap
    aspect="auto"             # Ensures the heatmap fills the container properly
)

# 4. Styling adjustments
fig_heatmap.update_layout(
    title='<b>Average CGPA by Skill Development and Co-Curricular Participation</b>',
    title_x=0.5, # Centers the title
    xaxis_title='Co-Curricular Participation',
    yaxis_title='Skill Development Hours Category'
)

# 5. Display in Streamlit
st.plotly_chart(fig_heatmap, use_container_width=True)
