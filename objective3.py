import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="UMK Learning Mode Analysis",
    layout="wide"
)

# ---------------------------------------
# TITLE & OBJECTIVES
# ---------------------------------------
st.title("🎓 UMK Student Learning Mode & Performance Analysis")

col_obj, col_prob = st.columns(2)

with col_obj:
    st.subheader("🎯 Objective")
    st.markdown("""
    This analysis examines how UMK students’ learning mode preferences—online, physical, or hybrid—are 
    distributed across the student population and how these preferences relate to academic performance. 
    By incorporating demographic factors, particularly year of study, this analysis explores whether 
    learning mode choices differ among student groups.
    """)

with col_prob:
    st.subheader("⚠️ Problem Statement")
    st.markdown("""
    UMK students have different learning mode preferences, but how these relate to academic performance 
    is not clearly understood. Learning mode choices may vary by year of study, potentially affecting 
    academic outcomes. Visual analysis is needed to identify these distributions and GPA differences.
    """)
st.markdown("---")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
# Ensure your CSV is named correctly or use your specific URL
# df = pd.read_csv("your_data.csv") 

# ---------------------------------------
# BLOCK STYLE SETTINGS
# ---------------------------------------
block_style = """
    background: linear-gradient(135deg, #1e3d59, #2e7d32);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
"""

# =====================================================
# 📊 SUMMARY INSIGHT BLOCK BOXES
# =====================================================
st.subheader("📊 Key Summary Insights")

# Compute metrics (adjust column names as per your dataset)
total_students = len(df)
avg_gpa = df['GPA_Numeric'].mean()
top_mode = df['Learning_Mode'].mode()[0]
top_gpa_group = "Year 1 Offline" # Based on your heatmap insight

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div style="{block_style}"><h3>👥 Total Students</h3><p style="font-size:20px; font-weight:bold;">{total_students}</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div style="{block_style}"><h3>📈 Average GPA</h3><p style="font-size:20px; font-weight:bold;">{avg_gpa:.2f}</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div style="{block_style}"><h3>🏆 Preferred Mode</h3><p style="font-size:20px; font-weight:bold;">{top_mode}</p></div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div style="{block_style}"><h3>⭐ Peak Group</h3><p style="font-size:20px; font-weight:bold;">{top_gpa_group}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 1️⃣ Pie Chart: Distribution of Learning Mode
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Pie Chart: Distribution of Learning Mode</h3></div>', unsafe_allow_html=True)

fig_pie = px.pie(df, names='Learning_Mode', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_pie, use_container_width=True)

if st.checkbox("Show Distribution Description", value=True, key="desc1"):
    st.markdown(f"""
    ### 📈 Distribution Description
    - The data reveals that **{top_mode}** is the dominant choice among students, accounting for over half the population.
    - This suggests a strong preference for a "middle ground" that combines digital flexibility with physical interaction.
    """)

st.markdown("---")

# =====================================================
# 2️⃣ Bar & Box Chart: GPA by Learning Mode
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Bar Chart: Average GPA by Learning Mode</h3></div>', unsafe_allow_html=True)

col_bar, col_box = st.columns(2)

with col_bar:
    avg_gpa_mode = df.groupby('Learning_Mode')['GPA_Numeric'].mean().reset_index()
    fig_bar = px.bar(avg_gpa_mode, x='Learning_Mode', y='GPA_Numeric', color='Learning_Mode', text_auto='.2f', title="Average GPA")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_box:
    fig_box = px.box(df, x='Learning_Mode', y='GPA_Numeric', color='Learning_Mode', title="GPA Variance (Spread)")
    st.plotly_chart(fig_box, use_container_width=True)

if st.checkbox("Show Performance Interpretation", value=True, key="desc2"):
    st.markdown("""
    ### 📈 Analytic Interpretation
    - **Performance Stability:** Average GPAs are remarkably consistent across modes (~3.40), suggesting that learning mode choice does not inherently disadvantage a student's average score.
    - **Variance:** The Offline mode shows a wider spread in the box plot, indicating that while many excel, there is a higher degree of performance variability compared to the Hybrid group.
    """)

st.markdown("---")

# =====================================================
# 3️⃣ Histogram: Preference by Year of Study
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ Histogram: Learning Mode Preference by Year of Study</h3></div>', unsafe_allow_html=True)

fig_hist = px.histogram(df, x='Year_of_Study', color='Learning_Mode', barmode='stack')
fig_hist.update_xaxes(type='category')
st.plotly_chart(fig_hist, use_container_width=True)

if st.checkbox("Show Year-on-Year Description", value=True, key="desc3"):
    st.markdown("""
    ### 📈 Distribution Description
    - As students progress from Year 1 to Year 4, the preference for **Hybrid** learning grows significantly.
    - Year 1 students show a higher proportional interest in **Offline** learning, likely due to the need for campus orientation and foundational social integration.
    """)

st.markdown("---")

# =====================================================
# 4️⃣ Heatmap: GPA by Mode and Year
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Heatmap: Average GPA by Learning Mode & Year</h3></div>', unsafe_allow_html=True)

gpa_heatmap_data = df.groupby(['Learning_Mode', 'Year_of_Study'])['GPA_Numeric'].mean().reset_index()
fig_heatmap = px.density_heatmap(
    gpa_heatmap_data, x='Year_of_Study', y='Learning_Mode', z='GPA_Numeric', 
    text_auto='.2f', color_continuous_scale='Viridis'
)
fig_heatmap.update_xaxes(type='category')
st.plotly_chart(fig_heatmap, use_container_width=True)

if st.checkbox("Show Matrix Interpretation", value=True, key="desc4"):
    st.markdown("""
    ### 📈 Distribution Description
    - **Peak Achievement:** Year 1 students in the **Offline** mode record the highest average GPA (3.85).
    - **Risk Factor:** A notable decline is observed in **Year 4 Online** students (3.04), suggesting that complex final-year coursework may be harder to master without physical peer or faculty support.
    - **Consistent Success:** The Hybrid mode maintains a stable performance matrix across all four years.
    """)

st.markdown("---")

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown(
    "This dashboard provides interactive visual insights into how learning modes "
    "and year of study influence UMK students' academic performance."
)
