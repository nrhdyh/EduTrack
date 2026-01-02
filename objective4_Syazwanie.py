import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Skill Development & Performance Analysis",
    layout="wide",
    page_icon="💜"
)

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

#---------------------------------------
# TITLE & OVERVIEW
#---------------------------------------
st.title("💜 Skill Development & Academic Outcomes")
st.markdown("""
This analysis explores the relationship between co-curricular activities, skill development hours, 
and academic performance (CGPA) among UMK students.
""")
st.markdown("---")

# =====================================================
# 🎨 PURPLE/LILAC THEME STYLE BLOCK
# =====================================================
# Gradient from deep purple to soft lilac
block_style = """
    background: linear-gradient(135deg, #663399, #B094C9); 
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3); /* Adds contrast for readability */
"""

# =====================================================
# 📊 SUMMARY INSIGHTS (Filtered)
# =====================================================
st.subheader("🎆 Key Summary Insights")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    selected_year = st.selectbox("Filter by Year", ["All"] + sorted(df["Year_of_Study"].dropna().unique().tolist()))
with col_f2:
    selected_skill = st.selectbox("Filter by Skill Category", ["All"] + sorted(df["Skills_Category"].dropna().unique().tolist()))
with col_f3:
    selected_active = st.selectbox("Filter by Activity", ["All"] + sorted(df["Co_Curriculum_Activities_Text"].dropna().unique().tolist()))

filtered_df = df.copy()
if selected_year != "All": filtered_df = filtered_df[filtered_df["Year_of_Study"] == selected_year]
if selected_skill != "All": filtered_df = filtered_df[filtered_df["Skills_Category"] == selected_skill]
if selected_active != "All": filtered_df = filtered_df[filtered_df["Co_Curriculum_Activities_Text"] == selected_active]

avg_cgpa = filtered_df["CGPA_Midpoint"].mean() if not filtered_df.empty else 0
total_students = len(filtered_df)
active_pct = (len(filtered_df[filtered_df["Co_Curriculum_Activities_Text"] == "Yes"]) / total_students * 100) if total_students > 0 else 0
max_cgpa = filtered_df["CGPA_Midpoint"].max() if not filtered_df.empty else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div style="{block_style}"><h5>👥 Total Students</h5><p style="font-size:20px; font-weight:bold;">{total_students}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{block_style}"><h5>📈 Avg CGPA</h5><p style="font-size:20px; font-weight:bold;">{avg_cgpa:.2f}</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{block_style}"><h5>🌟 Active Pct</h5><p style="font-size:20px; font-weight:bold;">{active_pct:.1f}%</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{block_style}"><h5>🔥 Max CGPA</h5><p style="font-size:20px; font-weight:bold;">{max_cgpa:.2f}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 1️⃣ Performance Density (Histogram/KDE)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Performance Density: Active vs Non-Active</h3></div>', unsafe_allow_html=True)

fig1 = px.histogram(
    filtered_df, 
    x='CGPA_Midpoint', 
    color='Co_Curriculum_Activities_Text',
    marginal="violin", 
    histnorm='probability density',
    barmode='overlay',
    # Using distinct purple shades for Yes/No
    color_discrete_sequence=["#8A2BE2", "#D8BFD8"], # BlueViolet & Thistle (Lilac)
    title='Density Distribution of CGPA'
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# 2️⃣ Grouped Bar Chart
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Skill Dev & Participation</h3></div>', unsafe_allow_html=True)

df_grouped = filtered_df.groupby(['Skill_Development_Hours_Category', 'Co_Curriculum_Activities_Text'])['CGPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    df_grouped,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    barmode='group',
    # Stronger purple contrast
    color_discrete_sequence=["#6A0DAD", "#C8A2C8"], # Deep Purple & Lilac
    text_auto='.2f'
)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3️⃣ Stacked Horizontal Bar (Distribution)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Ranges by Skill Category</h3></div>', unsafe_allow_html=True)

# --- Data Prep ---
cgpa_order = ['2.50 – 2.99', '3.00 – 3.69', '3.70 - 4.00']
cross_tab = pd.crosstab(filtered_df['Skills_Category'], filtered_df['CGPA'])
available_order = [c for c in cgpa_order if c in cross_tab.columns]
cross_tab = cross_tab[available_order]

percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0).reset_index()
df_melted = percentage_dist.melt(id_vars='Skills_Category', var_name='CGPA Range', value_name='Percentage')
df_melted['Percentage'] *= 100
# -----------------

fig3 = px.bar(
    df_melted,
    y='Skills_Category',
    x='Percentage',
    color='CGPA Range',
    orientation='h',
    text_auto='.1f',
    # NOTE: Keeping Red/Yellow/Green as these are performance indicators, not thematic elements.
    color_discrete_map={
        available_order[0]: '#e74c3c', 
        available_order[1]: '#f1c40f', 
        available_order[2]: '#2ecc71'
    }
)
st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# 4️⃣ Violin Plot
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ CGPA Density: Skill Levels vs Participation</h3></div>', unsafe_allow_html=True)

fig4 = px.violin(
    filtered_df,
    x='Skill_Development_Hours_Category',
    y='CGPA_Midpoint',
    color='Co_Curriculum_Activities_Text',
    box=True,
    points=None,
    # Medium purple and lighter lavender
    color_discrete_sequence=["#9370DB", "#E6E6FA"] 
)
# Add horizontal baseline for average with a purple hue line
fig4.add_hline(y=df['CGPA_Midpoint'].mean(), line_dash="dash", line_color="#4B0082", annotation_text="Global Avg")
st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# 5️⃣ Line Plot: Academic Progression
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ Academic Progression Trends</h3></div>', unsafe_allow_html=True)

df_line = filtered_df.groupby(['Year_of_Study', 'Skill_Development_Hours_Category'])['CGPA_Midpoint'].mean().reset_index()

fig5 = px.line(
    df_line,
    x='Year_of_Study',
    y='CGPA_Midpoint',
    color='Skill_Development_Hours_Category',
    markers=True,
    # Using Plotly's built-in sequential purple scale
    color_discrete_sequence=px.colors.sequential.Purples_r
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.caption("💜 EduTrack Analytics | Custom Purple & Lilac Theme Dashboard")
