import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="UMK Student Performance Analytics",
    layout="wide"
)

# ---------------------------------------
# HELPER FUNCTION
# ---------------------------------------
def sort_by_lower_bound(value):
    try:
        # Handling ranges like "3.50-4.00" or ">6 hours"
        clean_val = str(value).split("-")[0].strip().replace("%", "").replace(">", "").replace(" hours", "")
        return float(clean_val)
    except:
        return 0

# ---------------------------------------
# STYLE DEFINITION
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
# TITLE & INTRODUCTION
# ---------------------------------------
st.title("🎓 Impact of Holistic Development on UMK Students' Academic Performance")

st.markdown("### 🎯 Objective")
st.info("To evaluate the impact of skill development and co-curricular participation on UMK students' academic performance.")

st.markdown("### ❗ Problem Statement")
st.markdown("""
*While UMK emphasizes holistic student development, there is a lack of empirical evidence regarding how the time invested in non-academic skill development and participation in co-curricular activities correlates with academic success. Students often face a dilemma in balancing extracurricular commitments with their studies, leading to uncertainty about whether these activities enhance academic performance through soft skill acquisition or hinder it due to time constraints.*
""")
st.markdown("---")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

# ---------------------------------------
# 📊 KEY METRICS (SUMMARY INSIGHT BLOCKS)
# ---------------------------------------
st.subheader("📊 Key Metrics")

# Compute metrics
avg_cgpa = df["CGPA_Midpoint"].mean()
active_count = len(df[df['Co_Curriculum_Activities_Text'] == 'Yes'])
active_pct = (active_count / len(df)) * 100
correlation = df['CGPA_Midpoint'].corr(df['GPA_Midpoint'])
top_skill_group = df['Skill_Development_Hours_Category'].mode()[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div style="{block_style}"><h5>📈 Avg CGPA</h5><p style="font-size:20px; font-weight:bold;">{avg_cgpa:.2f}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{block_style}"><h5>🔥 Participation Rate</h5><p style="font-size:20px; font-weight:bold;">{active_pct:.1f}%</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{block_style}"><h5>🔗 Academic Correlation</h5><p style="font-size:20px; font-weight:bold;">{correlation:.2f}</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{block_style}"><h5>🛠️ Predominant Skill</h5><p style="font-size:20px; font-weight:bold;">{top_skill_group}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------
# DATA PREVIEW
# ---------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())
st.markdown("---")


# =====================================================
# 1️⃣ Population Distribution of CGPA (KDE Overlap Plot)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Population Distribution of CGPA (KDE Overlap Plot)</h3></div>', unsafe_allow_html=True)

active_students = df[df['Co_Curriculum_Activities_Text'] == 'Yes']['CGPA_Midpoint'].dropna()
non_active_students = df[df['Co_Curriculum_Activities_Text'] == 'No']['CGPA_Midpoint'].dropna()

fig1 = ff.create_distplot(
    [active_students, non_active_students], 
    ['Active (Yes)', 'Non-Active (No)'], 
    show_hist=False, show_rug=False, 
    colors=['#3B738F', '#6BBBA1']
)
fig1.update_layout(xaxis_title='CGPA Midpoint', yaxis_title='Density', template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)

if st.checkbox("Show Summary Statistics", value=True, key="stats1"):
    st.dataframe(df.groupby('Co_Curriculum_Activities_Text')['CGPA_Midpoint'].describe(), use_container_width=True)

if st.checkbox("Distribution Description", value=True, key="desc1"):
    st.markdown("""
    ### 📈 Interpretation
    The distribution curve for **"Active"** students displays a distinct rightward displacement along the CGPA axis. While the **"Inactive"** group peaks within the middle-performance tier, the mode—or most frequent score—for active students is physically shifted toward the **3.5–4.0 range**.
    
    This visualization identifies a significant **"Population Shift."** It demonstrates that the common fear of time constraints is statistically outweighed by a **"Performance Floor"** effect. A critical observation is the narrowing of the curve’s "tail" at the lower end for active students; they show a substantially lower probability of falling into the "at-risk" (sub-2.5) category. This suggests that co-curricular engagement acts as a **stabilizing force**.
    """)

st.markdown("---")

# =====================================================
# 2️⃣ Average CGPA by Activity & Skills (Grouped Bar Chart)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Skill Level and Participation</h3></div>', unsafe_allow_html=True)

df_grouped = df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()
fig2 = px.bar(
    df_grouped, x='Skill_Development_Hours_Category', y='CGPA_Midpoint', 
    color='Co_Curriculum_Activities_Text', barmode='group',
    color_discrete_sequence=px.colors.qualitative.Prism,
    category_orders={"Skill_Development_Hours_Category": ["Low", "Medium", "High"]}
)
st.plotly_chart(fig2, use_container_width=True)

if st.checkbox("Show Summary Statistics", value=True, key="stats2"):
    st.dataframe(df_grouped, use_container_width=True)

if st.checkbox("Distribution Description", value=True, key="desc2"):
    st.markdown("""
    ### 📈 Interpretation
    The data reveals a consistent **"Step-Ladder Trend."** As daily skill development hours increase from **"Low" to "High,"** CGPA midpoints rise in tandem. Crucially, the **"Active"** sub-group consistently holds the highest position on every level of the ladder, regardless of the hours committed.
    
    This chart effectively solves the **"Efficiency Paradox."** If the theory that extracurriculars hinder study were true, we would expect to see a "U-shaped" curve where grades drop once skill-building exceeds a certain threshold. Instead, the linear increase suggests a strong **positive correlation** between non-academic investment and academic output.
    """)

st.markdown("---")

# =====================================================
# 3️⃣ Percentage Distribution of CGPA Ranges (Stacked Bar)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Range Distribution by Skill Category</h3></div>', unsafe_allow_html=True)

actual_labels = sorted(df['CGPA'].unique().tolist())
cross_tab = pd.crosstab(df['Skills_Category'], df['CGPA'])[actual_labels]
percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
df_plot = percentage_dist.reset_index().melt(id_vars='Skills_Category', var_name='CGPA Range', value_name='Percentage')

colors_map = {'#e74c3c', '#f1c40f', '#2ecc71'} # Generic map
fig3 = px.bar(
    df_plot, y='Skills_Category', x='Percentage', color='CGPA Range', 
    orientation='h', text=df_plot['Percentage'].apply(lambda x: f'{x:.1f}%' if x > 0 else ''),
    color_discrete_sequence=px.colors.diverging.RdYlGn
)
st.plotly_chart(fig3, use_container_width=True)

if st.checkbox("Show Summary Statistics", value=True, key="stats3"):
    st.dataframe(percentage_dist, use_container_width=True)

if st.checkbox("Distribution Description", value=True, key="desc3"):
    st.markdown("""
    ### 📈 Interpretation
    There is a visible **"Proportional Expansion"** of the elite grade bracket (3.70–4.00). As skill levels move from **Low to High**, the share of students achieving top-tier honors often doubles or triples in its total percentage of the group.
    
    This highlights the existence of an **"Elite Pipeline."** High skill development is a primary predictor of **"First Class"** honors. The dramatic shrinkage of the **"<2.5"** bracket in the high-skill group suggests that holistic development is the most effective academic safety net available.
    """)

st.markdown("---")

# =====================================================
# 4️⃣ CGPA Density: Split Violin Plot
# =====================================================
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
fig4.update_layout(violinmode='overlay', template='plotly_white', title="Split Violin Plot: Skill Hours vs participation")
st.plotly_chart(fig4, use_container_width=True)

if st.checkbox("Show Summary Statistics", value=True, key="stats4"):
    st.dataframe(df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].describe(), use_container_width=True)

if st.checkbox("Distribution Description", value=True, key="desc4"):
    st.markdown("""
    ### 📈 Interpretation
    The density distribution for active students is noticeably **"Top-Heavy,"** with the bulk of the population concentrated in high-performance zones. Conversely, the inactive side is more **"Bulbous"** in the middle.
    
    The key insight here is the **Lower Variance** among active students. The inner quartile range is tighter and positioned higher for those engaged in co-curriculars. This suggests that participation **standardizes success**. For active students, external commitments force a level of **Internal Regulation** that turns high grades into a consistent habit.
    """)

st.markdown("---")

# =====================================================
# 5️⃣ Academic Progression (Line Plot)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ CGPA Trends Over Four Years (Academic Progression)</h3></div>', unsafe_allow_html=True)

df_line = df.groupby(['Year_of_Study', 'Skill_Development_Hours_Category'])['CGPA_Midpoint'].mean().reset_index()
fig5 = px.line(
    df_line, x='Year_of_Study', y='CGPA_Midpoint', 
    color='Skill_Development_Hours_Category', markers=True,
    category_orders={"Skill_Development_Hours_Category": ["Low", "Medium", "High"]}
)
st.plotly_chart(fig5, use_container_width=True)

if st.checkbox("Show Summary Statistics", value=True, key="stats5"):
    st.dataframe(df_line, use_container_width=True)

if st.checkbox("Distribution Description", value=True, key="desc5"):
    st.markdown("""
    ### 📈 Interpretation
    A clear **"Persistence Gap"** emerges as students move through their degree program. While high-skill students maintain a stable or ascending trajectory, low-skill students often experience a **"Junior Slump"** in Year 3 or 4.
    
    This is where **Soft Skill Acquisition** (leadership, initiative, and grit) transitions from being a "bonus" to a core requirement for academic survival. The widening gap in later years suggests that the benefits of holistic development are **Cumulative**, building a **"Resilience Buffer"** against peak workloads.
    """)

st.markdown("---")
st.markdown("💡 *This dashboard provides interactive insights into how holistic development factors influence UMK students' academic excellence.*")
