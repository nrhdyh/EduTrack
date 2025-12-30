import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Learning Mode Analysis",
    layout="wide",
    page_icon="🎓"
)

# ---------------------------------------
# TITLE & OVERVIEW SECTION
# ---------------------------------------
st.title("🎓 Learning Mode Preference, Demographic Factors & Academic Outcomes among UMK Students")

st.markdown("### 📝 Overview")
st.info("""
Learning mode preference plays an important role in shaping students’ learning experiences and academic outcomes. 
At Universiti Malaysia Kelantan (UMK), students adopt different learning modes, including online, physical, and 
hybrid learning, and these preferences may vary across demographic factors such as year of study. 

However, limited visual analysis has examined learning mode distribution, differences in GPA, variability in 
academic performance, and the combined effects of learning mode and demographic factors on student outcomes. 
This study aims to explore these relationships through data visualization to identify academic performance 
patterns and support informed academic planning.
""")

st.markdown("---")

# ---------------------------------------
# STYLE DEFINITION (Friend's Style)
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

# Calculations based on provided insights
total_students = len(df)
avg_gpa = df['GPA_Midpoint'].mean()
top_mode = "Hybrid"  
peak_performance = 3.85 

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div style="{block_style}"><h3>👥 Total Students</h3><p style="font-size:20px; font-weight:bold;">{total_students}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{block_style}"><h3>📈 Avg GPA</h3><p style="font-size:20px; font-weight:bold;">{avg_gpa:.2f}</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{block_style}"><h3>🏆 Dominant Mode</h3><p style="font-size:20px; font-weight:bold;">{top_mode}</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{block_style}"><h3>🔥 Peak GPA</h3><p style="font-size:20px; font-weight:bold;">{peak_performance}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 1️⃣ PIE CHART: Learning Mode Distribution
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Learning Mode Preference Distribution</h3></div>', unsafe_allow_html=True)

fig1 = px.pie(df, names='Learning_Mode', hole=0.4, 
             color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig1, use_container_width=True)

if st.checkbox("Show Distribution Description", value=True, key="desc1"):
    st.markdown(f"""
### 📈 Distribution Description
The student body shows a clear leaning toward flexible learning structures.
- **Hybrid Learning (54.4%)**: More than half the population prefers this mode, suggesting a strong desire for a balance between online flexibility and campus interaction.
- **Offline Learning (36.9%)**: Remains a significant preference, showing that a large portion of students still values traditional classroom engagement.
- **Online Learning (8.7%)**: Represents the smallest group, indicating that fully remote learning is the least preferred choice among UMK students.
""")

st.markdown("---")

# =====================================================
# 2️⃣ BAR CHART: Average GPA by Learning Mode
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average GPA by Learning Mode</h3></div>', unsafe_allow_html=True)

avg_gpa_data = df.groupby('Learning_Mode')['GPA_Midpoint'].mean().reset_index()
fig2 = px.bar(avg_gpa_data, x='Learning_Mode', y='GPA_Midpoint', 
             color='Learning_Mode', text_auto='.2f', 
             color_discrete_sequence=px.colors.sequential.Viridis)
st.plotly_chart(fig2, use_container_width=True)

if st.checkbox("Show Average GPA Interpretation", value=True, key="desc2"):
    st.markdown("""
### 📈 Average GPA Interpretation
- **Performance Stability**: Average GPAs across all modes hover consistently around the **3.40** range. This suggests that the chosen learning mode does not create a drastic gap in average academic outcomes.
- **The Offline Advantage**: Offline mode leads slightly with an average of approximately **3.48**, indicating high effectiveness for student success.
""")

st.markdown("---")

# =====================================================
# 3️⃣ BOX PLOT: GPA Distribution (Variability)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ GPA Distribution by Learning Mode (Variability)</h3></div>', unsafe_allow_html=True)

fig3 = px.box(df, x='Learning_Mode', y='GPA_Midpoint', color='Learning_Mode', 
             color_discrete_sequence=px.colors.sequential.Viridis)
st.plotly_chart(fig3, use_container_width=True)

if st.checkbox("Show Variability Interpretation", value=True, key="desc3"):
    st.markdown("""
### 📈 Variability Interpretation
- **Variance**: The Box Plot reveals a wider spread in the Offline mode, suggesting that while some students reach very high peaks, others may struggle more in this environment.
- **Predictability**: Hybrid results are more clustered around the median, showing that the Hybrid mode provides a more predictable performance level for the majority of students.
""")

st.markdown("---")

# =====================================================
# 4️⃣ STACKED BAR: Preference by Year of Study
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Learning Mode Preference by Year of Study</h3></div>', unsafe_allow_html=True)

fig4 = px.histogram(df, x='Year_of_Study', color='Learning_Mode', 
                   barmode='stack', title="Preference Trends Across Academic Years")
st.plotly_chart(fig4, use_container_width=True)

if st.checkbox("Show Year-on-Year Description", value=True, key="desc4"):
    st.markdown("""
### 📈 Distribution Description
This longitudinal view highlights how seniority affects choice:
- **Year 1**: Shows a relatively higher reliance on physical presence compared to later years.
- **Shift to Hybrid**: As students progress to **Year 3 and Year 4**, the preference for Hybrid learning expands significantly, likely as students become more independent and look for better time management.
- **Total Representation**: The overall number of students choosing Hybrid grows proportionally across the years, cementing it as the most sustainable choice for senior levels.
""")

st.markdown("---")

# =====================================================
# 5️⃣ HEATMAP: Average GPA Success Matrix
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ Heatmap: Average GPA Success Matrix</h3></div>', unsafe_allow_html=True)

heatmap_data = df.groupby(['Learning_Mode', 'Year_of_Study'])['GPA_Midpoint'].mean().reset_index()
fig5 = px.density_heatmap(heatmap_data, x='Year_of_Study', y='Learning_Mode', z='GPA_Midpoint',
                         text_auto='.2f', color_continuous_scale="Viridis",
                         labels={'GPA_Midpoint': 'Avg GPA'})
st.plotly_chart(fig5, use_container_width=True)

if st.checkbox("Show Final Analytic Summary", value=True, key="desc5"):
    st.markdown("""
### 📈 Final Analytic Summary
The success matrix identifies critical peaks and risks:
- **The Peak (3.85)**: **Year 1 Offline students** record the highest performance in the entire dataset, suggesting that physical interaction is vital for building a strong foundation in the first year.
- **Stability**: Hybrid mode provides the most consistent GPA across all years (3.32 to 3.51), showing it is a reliable choice for long-term academic stability.
- **The Risk (3.04)**: A notable drop occurs for **Year 4 Online students**, which may indicate that advanced senior-level subjects are more difficult to master without physical peer or faculty support.
""")

st.markdown("---")
st.caption("Developed for UMK Educational Analytics Dashboard.")
