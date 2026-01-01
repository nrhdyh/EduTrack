import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="UMK Student Performance Dashboard",
    layout="wide"
)

# ---------------------------------------
# DATA LOADING
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

# ---------------------------------------
# DESIGN STYLE (Friend's Structure)
# ---------------------------------------
block_style = """
    background: linear-gradient(135deg, #5E35B1, #3949AB);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
"""

# ---------------------------------------
# TITLE & PROBLEM STATEMENT
# ---------------------------------------
st.title("🎓 Impact of Holistic Development on UMK Students' Academic Performance")

st.markdown(f"""
<div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 5px solid #5E35B1;">
    <h4>❗ Problem Statement</h4>
    <p>"While UMK emphasizes holistic student development, there is a lack of empirical evidence regarding how the time invested in non-academic skill development 
    and participation in co-curricular activities correlates with academic success. Students often face a dilemma in balancing extracurricular commitments 
    with their studies, leading to uncertainty about whether these activities enhance academic performance through soft skill acquisition or hinder it due to time constraints."</p>
    <br>
    <h4>🎯 Objective</h4>
    <p>To evaluate the impact of skill development and co-curricular participation on UMK students' academic performance.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------
# 📊 KEY METRICS (Friend's Summary Blocks)
# ---------------------------------------
st.subheader("📊 Key Metrics Summary")

# Calculations
avg_cgpa = df["CGPA_Midpoint"].mean()
active_pct = (len(df[df['Co_Curriculum_Activities_Text'] == 'Yes']) / len(df)) * 100
high_skill_pct = (len(df[df['Skill_Development_Hours_Category'] == 'High']) / len(df)) * 100
elite_students = (len(df[df['CGPA_Midpoint'] >= 3.70]) / len(df)) * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div style="{block_style}"><h5>📈 Avg CGPA</h5><p style="font-size:20px; font-weight:bold;">{avg_cgpa:.2f}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{block_style}"><h5>🔥 Active Rate</h5><p style="font-size:20px; font-weight:bold;">{active_pct:.1f}%</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{block_style}"><h5>🛠️ High Skill Dev</h5><p style="font-size:20px; font-weight:bold;">{high_skill_pct:.1f}%</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{block_style}"><h5>🏆 Elite Tier</h5><p style="font-size:20px; font-weight:bold;">{elite_students:.1f}%</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 1️⃣ VISUALIZATION 1: Performance Density (KDE)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Population Distribution of CGPA (KDE Overlap Plot)</h3></div>', unsafe_allow_html=True)

active_students = df[df['Co_Curriculum_Activities_Text'] == 'Yes']['CGPA_Midpoint'].dropna()
non_active_students = df[df['Co_Curriculum_Activities_Text'] == 'No']['CGPA_Midpoint'].dropna()

hist_data = [active_students, non_active_students]
group_labels = ['Active (Yes)', 'Non-Active (No)']
colors = ['#3B738F', '#6BBBA1']

fig1 = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False, colors=colors)
fig1.update_layout(xaxis_title='CGPA Midpoint', yaxis_title='Density', template='plotly_white', legend_title='Participation')
st.plotly_chart(fig1, use_container_width=True)

# Toggles
if st.checkbox("Show Summary Statistics", key="stats1"):
    st.dataframe(df.groupby('Co_Curriculum_Activities_Text')['CGPA_Midpoint'].describe(), use_container_width=True)

if st.checkbox("Show Interpretation Finding", key="desc1"):
    st.markdown("""
    ### 📈 Analysis
    The distribution curve for **"Active"** students displays a distinct rightward displacement along the CGPA axis. While the **"Inactive"** group peaks within the middle-performance tier, the mode—or most frequent score—for active students is physically shifted toward the **3.5–4.0 range**.
    
    This visualization identifies a significant **"Population Shift."** It demonstrates that the common fear of time constraints is statistically outweighed by a **"Performance Floor"** effect. A critical observation is the narrowing of the curve’s "tail" at the lower end for active students; they show a substantially lower probability of falling into the "at-risk" (sub-2.5) category. This suggests that co-curricular engagement acts as a **stabilizing force**. 
    """)

st.markdown("---")

# =====================================================
# 2️⃣ VISUALIZATION 2: Average CGPA (Grouped Bar)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Skill Level and Participation</h3></div>', unsafe_allow_html=True)

df_grouped = df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    df_grouped, x='Skill_Development_Hours_Category', y='CGPA_Midpoint', color='Co_Curriculum_Activities_Text',
    barmode='group', title='Average CGPA by Skill Development and Co-Curricular Participation',
    labels={'CGPA_Midpoint': 'Avg CGPA', 'Skill_Development_Hours_Category': 'Skill Hours'},
    color_discrete_sequence=px.colors.qualitative.Prism,
    category_orders={"Skill_Development_Hours_Category": ["Low", "Medium", "High"]}
)
st.plotly_chart(fig2, use_container_width=True)

if st.checkbox("Show Summary Statistics", key="stats2"):
    st.dataframe(df_grouped, use_container_width=True)

if st.checkbox("Show Interpretation Finding", key="desc2"):
    st.markdown("""
    ### 📈 Analysis
    The data reveals a consistent **"Step-Ladder Trend."** As daily skill development hours increase from **"Low" to "High,"** CGPA midpoints rise in tandem. Crucially, the **"Active"** sub-group consistently holds the highest position on every level of the ladder, regardless of the hours committed.
    
    This chart effectively solves the **"Efficiency Paradox."** If the theory that extracurriculars hinder study were true, we would expect to see a "U-shaped" curve where grades drop once skill-building exceeds a certain threshold. Instead, the linear increase suggests a strong **positive correlation** between non-academic investment and academic output.
    """)

st.markdown("---")

# =====================================================
# 3️⃣ VISUALIZATION 3: Percentage Distribution (Stacked Horizontal Bar)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Range Distribution by Skill Category</h3></div>', unsafe_allow_html=True)

actual_labels = sorted(df['CGPA'].unique().tolist())
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])[actual_labels]
percentage_dist = (cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100).reset_index()

df_plot = percentage_dist.melt(id_vars='Skills_Category', var_name='CGPA Range', value_name='Percentage')

fig3 = px.bar(
    df_plot, y='Skills_Category', x='Percentage', color='CGPA Range', orientation='h',
    title='Percentage Distribution of CGPA Ranges by Skill Category',
    color_discrete_sequence=px.colors.diverging.RdYlGn,
    category_orders={'CGPA Range': actual_labels},
    text=df_plot['Percentage'].apply(lambda x: f'{x:.1f}%' if x > 0 else '')
)
fig3.update_layout(xaxis_range=[0, 100], plot_bgcolor='white')
fig3.update_traces(textposition='inside', textfont=dict(color='black', family='Arial Black'))
st.plotly_chart(fig3, use_container_width=True)

if st.checkbox("Show Summary Statistics", key="stats3"):
    st.dataframe(percentage_dist, use_container_width=True)

if st.checkbox("Show Interpretation Finding", key="desc3"):
    st.markdown("""
    ### 📈 Analysis
    There is a visible **"Proportional Expansion"** of the elite grade bracket (3.70–4.00). As skill levels move from **Low to High**, the share of students achieving top-tier honors often doubles or triples in its total percentage of the group.
    
    This highlights the existence of an **"Elite Pipeline."** High skill development is a primary predictor of **"First Class"** honors. The dramatic shrinkage of the **"<2.5"** bracket in the high-skill group suggests that holistic development is the most effective academic safety net available.
    """)

st.markdown("---")

# =====================================================
# 4️⃣ VISUALIZATION 4: CGPA Density (Split Violin Plot)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Academic Performance Density and Consistency</h3></div>', unsafe_allow_html=True)

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

if st.checkbox("Show Summary Statistics", key="stats4"):
    st.dataframe(df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].describe(), use_container_width=True)

if st.checkbox("Show Interpretation Finding", key="desc4"):
    st.markdown("""
    ### 📈 Analysis
    The density distribution for active students is noticeably **"Top-Heavy,"** with the bulk of the population concentrated in high-performance zones. Conversely, the inactive side is more **"Bulbous"** in the middle.
    
    The key insight here is the **Lower Variance** among active students. The inner quartile range is tighter and positioned higher for those engaged in co-curriculars. This suggests that participation **standardizes success**. For active students, external commitments force a level of **Internal Regulation** that turns high grades into a consistent habit.
    """)

st.markdown("---")

# =====================================================
# 5️⃣ VISUALIZATION 5: Academic Progression (Line Plot)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ CGPA Trends Over Four Years (Academic Progression)</h3></div>', unsafe_allow_html=True)

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

if st.checkbox("Show Summary Statistics", key="stats5"):
    st.dataframe(df_line, use_container_width=True)

if st.checkbox("Show Interpretation Finding", key="desc5"):
    st.markdown("""
    ### 📈 Analysis
    A clear **"Persistence Gap"** emerges as students move through their degree program. While high-skill students maintain a stable or ascending trajectory, low-skill students often experience a **"Junior Slump"** in Year 3 or 4.
    
    Higher-level years involve more complex, self-directed learning. This is where **Soft Skill Acquisition**—specifically leadership, initiative, and grit—transitions from being a "bonus" to a core requirement for academic survival. The widening gap in later years suggests that the benefits of holistic development are **Cumulative**, building a **"Resilience Buffer"**.
    """)

st.markdown("---")
st.markdown("💡 *Data analysis based on UMK Student Survey. Designed with Streamlit & Plotly.*")
