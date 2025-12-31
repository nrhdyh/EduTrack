import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go  # Added missing import

# 1. Page Configuration & Design Style
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Friend's Design Style
block_style = """
    background: linear-gradient(135deg, #5E35B1, #3949AB);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
"""

st.title("🎓 Student Performance & Skill Development Analytics")

# 2. Problem Statement & Objective
st.markdown("### ❗ Problem Statement")
st.info("While UMK emphasizes holistic student development, there is a lack of empirical evidence regarding how the time invested in non-academic skill development and participation in co-curricular activities correlates with academic success...")

st.markdown("### 🎯 Objective")
st.markdown("> To evaluate the impact of skill development and co-curricular participation on UMK students' academic performance.")

# 3. Load Data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

# --- VISUALIZATION 1: Performance Density ---
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Performance Density: Active vs Non-Active</h3></div>', unsafe_allow_html=True)
active_students = df[df['Co_Curriculum_Activities_Text'] == 'Yes']['CGPA_Midpoint'].dropna()
non_active_students = df[df['Co_Curriculum_Activities_Text'] == 'No']['CGPA_Midpoint'].dropna()

fig1 = ff.create_distplot(
    [active_students, non_active_students], 
    ['Active (Yes)', 'Non-Active (No)'], 
    show_hist=False, show_rug=False, 
    colors=['#3B738F', '#6BBBA1']
)
st.plotly_chart(fig1, use_container_width=True)

if st.checkbox("Show Interpretation 1"):
    st.write("The distribution curve for 'Active' students displays a distinct rightward displacement...")

# --- VISUALIZATION 2: Average CGPA (Grouped Bar) ---
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Activity & Skills</h3></div>', unsafe_allow_html=True)
df_grouped = df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    df_grouped, x='Skill_Development_Hours_Category', y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text', barmode='group',
    color_discrete_sequence=px.colors.qualitative.Prism,
    category_orders={"Skill_Development_Hours_Category": ["Low", "Medium", "High"]}
)
st.plotly_chart(fig2, use_container_width=True)

# --- VISUALIZATION 3: Percentage Distribution ---
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Range Distribution by Skill Category</h3></div>', unsafe_allow_html=True)
actual_labels = sorted(df['CGPA'].unique().tolist())
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])[actual_labels]
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
df_plot = percentage_dist.reset_index().melt(id_vars='Skills_Category', var_name='CGPA Range', value_name='Percentage')

fig3 = px.bar(
    df_plot, y='Skills_Category', x='Percentage', color='CGPA Range', orientation='h',
    color_discrete_sequence=px.colors.diverging.RdYlGn,
    category_orders={'CGPA Range': actual_labels},
    text=df_plot['Percentage'].apply(lambda x: f'{x:.1f}%' if x > 0 else '')
)
fig3.update_layout(xaxis_range=[0, 100], plot_bgcolor='white')
st.plotly_chart(fig3, use_container_width=True)

# --- VISUALIZATION 4: Split Violin Plot ---
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Academic Performance Density and Consistency</h3></div>', unsafe_allow_html=True)
fig4 = go.Figure()
fig4.add_trace(go.Violin(
    x=df['Skill_Development_Hours_Category'][df['Co_Curriculum_Activities_Text'] == 'No'],
    y=df['CGPA_Midpoint'][df['Co_Curriculum_Activities_Text'] == 'No'],
    legendgroup='No', name='No', side='negative', line_color='blue', meanline_visible=True
))
fig4.add_trace(go.Violin(
    x=df['Skill_Development_Hours_Category'][df['Co_Curriculum_Activities_Text'] == 'Yes'],
    y=df['CGPA_Midpoint'][df['Co_Curriculum_Activities_Text'] == 'Yes'],
    legendgroup='Yes', name='Yes', side='positive', line_color='orange', meanline_visible=True
))
fig4.update_layout(violinmode='overlay', template='plotly_white')
st.plotly_chart(fig4, use_container_width=True) # Changed from fig.show()

# --- VISUALIZATION 5: Academic Progression ---
st.markdown(f'<div style="{block_style}"><h3>5️⃣ CGPA Trends Over Four Years</h3></div>', unsafe_allow_html=True)
df_line = df.groupby(['Year_of_Study', 'Skill_Development_Hours_Category'])['CGPA_Midpoint'].mean().reset_index()

fig5 = px.line(
    df_line, x='Year_of_Study', y='CGPA_Midpoint', color='Skill_Development_Hours_Category',
    markers=True, category_orders={"Skill_Development_Hours_Category": ["Low", "Medium", "High"]}
)
st.plotly_chart(fig5, use_container_width=True) # Added missing closing parenthesis
