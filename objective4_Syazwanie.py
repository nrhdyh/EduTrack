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
import plotly.figure_factory as ff
import streamlit as st

# 1. Prepare the data groups based on 'Co_Curriculum_Activities_Text'
# We extract the 'CGPA_Midpoint' for each category to pass into the distplot
active_students = df[df['Co_Curriculum_Activities_Text'] == 'Yes']['CGPA_Midpoint'].dropna()
non_active_students = df[df['Co_Curriculum_Activities_Text'] == 'No']['CGPA_Midpoint'].dropna()

hist_data = [active_students, non_active_students]
group_labels = ['Active (Yes)', 'Non-Active (No)']
colors = ['#3B738F', '#6BBBA1'] # Approximate 'crest' palette (teal/green)

# 2. Create the Distplot
# show_hist=False and show_rug=False replicate the pure KDE look
fig = ff.create_distplot(
    hist_data, 
    group_labels, 
    show_hist=False, 
    show_rug=False, 
    colors=colors
)

# 3. Add formatting
fig.update_layout(
    title='Performance Density: Active vs Non-Active students',
    xaxis_title='CGPA Midpoint',
    yaxis_title='Density',
    template='plotly_white',
    legend_title='Participation'
)

# 4. Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


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

# --- VISUALIZATION 4: CGPA Density : Skill Development Levels vs. Co-curricular Participation(Split Violin Plot) ---

# 1. Define the categories for the X-axis to maintain order
categories = df['Skill_Development_Hours_Category'].unique()

fig = go.Figure()

# 2. Add the "Left" side of the violin (e.g., Co-curricular: No)
fig.add_trace(go.Violin(
    x=df['Skill_Development_Hours_Category'][df['Co_Curriculum_Activities_Text'] == 'No'],
    y=df['CGPA_Midpoint'][df['Co_Curriculum_Activities_Text'] == 'No'],
    legendgroup='No', name='No',
    side='negative', # This puts it on the left
    line_color='blue',
    meanline_visible=True
))

# 3. Add the "Right" side of the violin (e.g., Co-curricular: Yes)
fig.add_trace(go.Violin(
    x=df['Skill_Development_Hours_Category'][df['Co_Curriculum_Activities_Text'] == 'Yes'],
    y=df['CGPA_Midpoint'][df['Co_Curriculum_Activities_Text'] == 'Yes'],
    legendgroup='Yes', name='Yes',
    side='positive', # This puts it on the right
    line_color='orange',
    meanline_visible=True
))

# 4. Add the Horizontal Mean Line (Baseline)
overall_mean = df['CGPA_Midpoint'].mean()
fig.add_hline(y=overall_mean, line_dash="dash", line_color="red", 
              annotation_text="Overall Average", annotation_position="bottom right")

# 5. Formatting the layout
fig.update_traces(box_visible=False, meanline_visible=True) # inner="quart" equivalent
fig.update_layout(
    title='CGPA Density: Skill Development Levels vs. Co-curricular Participation',
    xaxis_title='Skill Development Hours Category',
    yaxis_title='CGPA Midpoint',
    violinmode='overlay', # This is crucial to merge the two sides into one violin
    legend_title='Co-curricular Participation',
    template='plotly_white'
)

fig.show()


# --- VISUALIZATION 5: Academic Progression (Line Plot) ---

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
st.plotly_chart(fig5, use_container_width=True
