import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# DATA LOADING
# =====================================================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Learning Mode Analysis | UMK",
    layout="wide",
    page_icon="🎓"
)

# =====================================================
# TITLE & OVERVIEW
# =====================================================
st.title("🎓 Learning Mode Preference, Demographic Factors & Academic Outcomes Among UMK Students")

st.markdown("### 📝 Overview")
st.info("""
Learning mode preference plays an important role in shaping students’ learning experiences and academic outcomes. 
At Universiti Malaysia Kelantan (UMK), students adopt different learning modes including online, physical, and hybrid learning. 
These preferences may vary across demographic factors such as year of study and influence both short-term (GPA) and long-term (CGPA) academic performance.

This dashboard visually explores learning mode distribution, performance differences, variability, and year-based trends 
to support informed academic planning and decision-making.
""")

st.markdown("---")

# =====================================================
# STYLE BLOCK
# =====================================================
block_style = """
    background: linear-gradient(135deg, #1e3d59, #2e7d32);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
"""

# =====================================================
# SUMMARY METRICS
# =====================================================
st.subheader("📊 Key Summary Insights")

total_students = len(df)
avg_gpa = df['GPA_Midpoint'].mean()
top_mode = df['Learning_Mode'].mode()[0]
peak_cgpa = df['CGPA_Midpoint'].max()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div style="{block_style}"><h3>👥 Total Students</h3><p style="font-size:22px; font-weight:bold;">{total_students}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{block_style}"><h3>📈 Avg GPA</h3><p style="font-size:22px; font-weight:bold;">{avg_gpa:.2f}</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{block_style}"><h3>🏆 Dominant Mode</h3><p style="font-size:22px; font-weight:bold;">{top_mode}</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{block_style}"><h3>🔥 Peak CGPA</h3><p style="font-size:22px; font-weight:bold;">{peak_cgpa:.2f}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 1️⃣ PIE CHART: LEARNING MODE DISTRIBUTION
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Learning Mode Preference Distribution</h3></div>', unsafe_allow_html=True)

fig1 = px.pie(df, names='Learning_Mode', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig1, use_container_width=True)

c1, c2 = st.columns([1, 2])
with c1:
    st.write("**Summary Statistics:**")
    mode_counts = df['Learning_Mode'].value_counts(normalize=True) * 100
    st.write(f"- **Hybrid:** {mode_counts.get('Hybrid', 0):.1f}%")
    st.write(f"- **Offline:** {mode_counts.get('Offline', 0):.1f}%")
    st.write(f"- **Online:** {mode_counts.get('Online', 0):.1f}%")
with c2:
    st.write("**Analysis:**")
    st.write("""The pie chart illustrates a dominant preference for flexibility among UMK students. Hybrid Learning is the most popular choice, accounting for 54.4% of the student population, indicating a strong desire for a blended educational experience that combines digital convenience with campus interaction. Offline Learning follows significantly at 36.9%, showing that a substantial portion of students still values traditional classroom engagement. Conversely, Online Learning is the least preferred mode at only 8.7%. This distribution suggests that while students have moved away from fully remote models, they are not yet ready to return to entirely physical-only instruction.""")

st.markdown("---")

# =====================================================
# 2️⃣ BAR CHART: AVG CGPA BY MODE
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Learning Mode</h3></div>', unsafe_allow_html=True)

avg_cgpa_data = df.groupby('Learning_Mode')['CGPA_Midpoint'].mean().reset_index()
fig2 = px.bar(avg_cgpa_data, x='Learning_Mode', y='CGPA_Midpoint', color='Learning_Mode', text_auto='.2f', color_discrete_sequence=px.colors.sequential.Viridis)
fig2.update_layout(showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

c1, c2 = st.columns([1, 2])
with c1:
    st.write("**Summary Statistics:**")
    for index, row in avg_cgpa_data.iterrows():
        st.write(f"- **{row['Learning_Mode']} Average:** {row['CGPA_Midpoint']:.2f}")
with c2:
    st.write("**Analysis:**")
    st.write("""This bar chart evaluates academic performance consistency across different instructional mediums. The results indicate that the learning environment has a minimal impact on overall academic success, as all three modes maintain a competitive average CGPA near the 3.40 mark. Offline Learning leads slightly with the highest average of approximately 3.48, which may reflect the benefits of immediate faculty feedback and peer collaboration. Hybrid and Online modes follow closely behind. This uniformity suggests that UMK students are highly adaptable, achieving high-quality academic outcomes regardless of whether their courses are delivered in person or digitally.""")

st.markdown("---")

# =====================================================
# 3️⃣ BOX PLOT: CGPA DISTRIBUTION
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Distribution by Learning Mode (Variability)</h3></div>', unsafe_allow_html=True)

fig3 = px.box(df, x='Learning_Mode', y='CGPA_Midpoint', color='Learning_Mode', color_discrete_sequence=px.colors.sequential.Viridis)
fig3.update_layout(showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

c1, c2 = st.columns([1, 2])
with c1:
    st.write("**Box Plot Metrics:**")
    box_stats = df.groupby('Learning_Mode')['CGPA_Midpoint'].describe()[['min', '50%', 'max']]
    for mode, row in box_stats.iterrows():
        st.write(f"- **{mode}:** Median {row['50%']:.2f} (Range: {row['min']:.2f}-{row['max']:.2f})")
with c2:
    st.write("**Analysis:**")
    st.write("""The box plot provides deeper insight into the variability of student performance. While the median CGPA remains relatively stable across all groups, the Offline mode displays the greatest variance, represented by a much larger box and longer whiskers. This indicates that while Offline learning can lead to exceptionally high scores, it also carries a wider range of performance outcomes compared to the more "clustered" results seen in the Hybrid and Online groups. The Hybrid mode shows the most consistency, with fewer extremes, suggesting it provides a reliable and predictable environment for the majority of students to maintain their grades.""")

st.markdown("---")

# =====================================================
# 4️⃣ STACKED BAR: MODE BY YEAR
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Learning Mode Preference by Year of Study</h3></div>', unsafe_allow_html=True)

fig4 = px.histogram(df, x='Year_of_Study', color='Learning_Mode', barmode='stack', color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig4, use_container_width=True)

c1, c2 = st.columns([1, 2])
with c1:
    st.write("**Yearly Distribution:**")
    counts = df.groupby('Year_of_Study')['Learning_Mode'].count()
    for year, val in counts.items():
        st.write(f"- **Year {year}:** {val} Students")
with c2:
    st.write("**Analysis:**")
    st.write("""This visualization highlights a clear shift in student needs as they progress through their academic journey. Year 1 students show a relatively higher reliance on Offline and Hybrid modes as they establish their academic foundation. As students reach Year 3 and Year 4, there is a massive surge in the total number of students preferring Hybrid learning. This trend likely reflects senior students' need for greater schedule flexibility to balance advanced coursework, final-year projects, or internships. Notably, the preference for purely Online learning remains a small but consistent niche across all four years.""")

st.markdown("---")

# =====================================================
# 5️⃣ HEATMAP: CGPA SUCCESS MATRIX
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ Heatmap: Average CGPA Success Matrix</h3></div>', unsafe_allow_html=True)

heatmap_data = df.groupby(['Learning_Mode', 'Year_of_Study'])['CGPA_Midpoint'].mean().reset_index()
fig5 = px.density_heatmap(heatmap_data, x='Year_of_Study', y='Learning_Mode', z='CGPA_Midpoint', text_auto=".2f", color_continuous_scale="Viridis", labels={'CGPA_Midpoint': 'Avg CGPA'})
st.plotly_chart(fig5, use_container_width=True)

c1, c2 = st.columns([1, 2])
with c1:
    st.write("**Key Matrix Points:**")
    st.write("- **Max Avg:** 3.72 (Year 1, Offline)")
    st.write("- **Min Avg:** 3.04 (Year 4, Online)")
with c2:
    st.write("**Analysis:**")
    st.write("""The heatmap identifies specific "performance corridors" where students excel most. The highest academic density is found among Year 1 Offline students (3.72), reinforcing the idea that physical presence is crucial for new students adapting to university standards. Another high-performing segment is Year 2 Hybrid and Online students, both averaging 3.68. However, a significant academic risk is identified in Year 4 Online students, where the average CGPA drops to its lowest point of 3.04. This suggests that senior-level complexity may require more direct supervision than a fully online environment can provide.""")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("📊 UMK Student Performance Dashboard | Data Visualization Project")
