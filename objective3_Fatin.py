import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="Learning Mode Analysis",
    layout="wide"
)

# ---------------------------------------
# HELPER FUNCTION
# ---------------------------------------
def sort_by_lower_bound(value):
    try:
        return float(value.split("-")[0].strip().replace("%", ""))
    except:
        return 0

#---------------------------------------
# TITLE & OVERVIEW
#---------------------------------------
st.title("💗 Learning Mode Preference & Academic Outcomes")
st.markdown("""
Learning mode preference plays an important role in shaping students’ learning experiences and academic outcomes. 
At Universiti Malaysia Kelantan (UMK), students adopt different learning modes including online, physical, and hybrid learning. 
""")
st.markdown("---")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance_ver2.csv"
df = pd.read_csv(url)

# =====================================================
# 🎨 PINK THEME STYLE BLOCK
# =====================================================
# Updated to a professional Pink/Magenta gradient
block_style = """
    background: linear-gradient(135deg, #FF69B4, #C71585);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
"""

# =====================================================
# 📊 SUMMARY INSIGHTS (Filtered)
# =====================================================
st.subheader("🌸 Key Summary Insights")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    selected_year = st.selectbox("Filter by Year", ["All"] + sorted(df["Year_of_Study"].dropna().unique().tolist()))
with col_f2:
    selected_faculty = st.selectbox("Filter by Faculty", ["All"] + sorted(df["Faculty_Short"].dropna().unique().tolist()))
with col_f3:
    selected_gender = st.selectbox("Filter by Gender", ["All"] + sorted(df["Gender"].dropna().unique().tolist()))

filtered_df = df.copy()
if selected_year != "All": filtered_df = filtered_df[filtered_df["Year_of_Study"] == selected_year]
if selected_faculty != "All": filtered_df = filtered_df[filtered_df["Faculty_Short"] == selected_faculty]
if selected_gender != "All": filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

avg_gpa = filtered_df["GPA_Midpoint"].mean() if not filtered_df.empty else 0
dominant_mode = filtered_df["Learning_Mode"].mode()[0] if not filtered_df.empty else "N/A"
max_cgpa = filtered_df["CGPA_Midpoint"].max() if not filtered_df.empty else 0
total_count = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div style="{block_style}"><h5>👥 Total Sample</h5><p style="font-size:20px; font-weight:bold;">{total_count}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{block_style}"><h5>📈 Avg GPA</h5><p style="font-size:20px; font-weight:bold;">{avg_gpa:.2f}</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{block_style}"><h5>🏆 Dominant Mode</h5><p style="font-size:20px; font-weight:bold;">{dominant_mode}</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{block_style}"><h5>🔥 Peak CGPA</h5><p style="font-size:20px; font-weight:bold;">{max_cgpa:.2f}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 1️⃣ Pie Chart: Pink Style
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Learning Mode Preference Distribution</h3></div>', unsafe_allow_html=True)

# Using 'RdPu' (Red-Purple) or 'Pinkyl' for pink tones
fig1 = px.pie(df, names='Learning_Mode', hole=0.4, 
             color_discrete_sequence=px.colors.sequential.RdPu_r)
st.plotly_chart(fig1, use_container_width=True)

if st.checkbox("Show distribution description", value=True, key="desc1"):
    st.markdown("""
The pie chart illustrates a dominant preference for flexibility among UMK students. Hybrid Learning is the most popular choice, accounting for 54.4% of the student population, indicating a strong desire for a blended educational experience that combines digital convenience with campus interaction. Offline Learning follows significantly at 36.9%, showing that a substantial portion of students still values traditional classroom engagement. Conversely, Online Learning is the least preferred mode at only 8.7%. This distribution suggests that while students have moved away from fully remote models, they are not yet ready to return to entirely physical-only instruction.
    """)

# =====================================================
# 2️⃣ Bar Chart: Pink/Sunset Style
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Bar Chart: Average CGPA by Learning Mode</h3></div>', unsafe_allow_html=True)

avg_cgpa_data = df.groupby('Learning_Mode')['CGPA_Midpoint'].mean().reset_index()
fig2 = px.bar(avg_cgpa_data, x='Learning_Mode', y='CGPA_Midpoint', 
             color='CGPA_Midpoint', text_auto='.2f', 
             color_continuous_scale="RdPu") # Pink scale
st.plotly_chart(fig2, use_container_width=True)

if st.checkbox("Show performance description", value=True, key="desc2"):
    st.markdown("""
This bar chart evaluates academic performance consistency across different instructional mediums. The results indicate that the learning environment has a minimal impact on overall academic success, as all three modes maintain a competitive average CGPA near the 3.40 mark. Offline Learning leads slightly with the highest average of approximately 3.48, which may reflect the benefits of immediate faculty feedback and peer collaboration. Hybrid and Online modes follow closely behind. This uniformity suggests that UMK students are highly adaptable, achieving high-quality academic outcomes regardless of whether their courses are delivered in person or digitally.
    """)

# =====================================================
# 3️⃣ Box Plot: Pink Style
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ Box Plot: CGPA Distribution by Learning Mode</h3></div>', unsafe_allow_html=True)

fig3 = px.box(df, x='Learning_Mode', y='CGPA_Midpoint', color='Learning_Mode',
             color_discrete_sequence=px.colors.qualitative.Prism) # Vibrant pinks/purples
st.plotly_chart(fig3, use_container_width=True)

if st.checkbox("Show variability description", value=True, key="desc3"):
    st.markdown("""
The box plot provides deeper insight into the variability of student performance. While the median CGPA remains relatively stable across all groups, the Offline mode displays the greatest variance, represented by a much larger box and longer whiskers. This indicates that while Offline learning can lead to exceptionally high scores, it also carries a wider range of performance outcomes compared to the more "clustered" results seen in the Hybrid and Online groups. The Hybrid mode shows the most consistency, with fewer extremes, suggesting it provides a reliable and predictable environment for the majority of students to maintain their grades.
    """)

# =====================================================
# 4️⃣ Heatmap: Pink Style
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Heatmap: Average CGPA Success Matrix</h3></div>', unsafe_allow_html=True)

heatmap_data = df.groupby(['Learning_Mode', 'Year_of_Study'])['CGPA_Midpoint'].mean().reset_index()
fig5 = px.density_heatmap(heatmap_data, x='Year_of_Study', y='Learning_Mode', z='CGPA_Midpoint',
                         text_auto=".2f", color_continuous_scale="PuRd") # Purple-Red/Pink
st.plotly_chart(fig5, use_container_width=True)

if st.checkbox("Show heatmap description", value=True, key="desc5"):
    st.markdown("""
The heatmap identifies specific "performance corridors" where students excel most. The highest academic density is found among Year 1 Offline students (3.72), reinforcing the idea that physical presence is crucial for new students adapting to university standards. Another high-performing segment is Year 2 Hybrid and Online students, both averaging 3.68. However, a significant academic risk is identified in Year 4 Online students, where the average CGPA drops to its lowest point of 3.04. This suggests that senior-level complexity may require more direct supervision than a fully online environment can provide.
    """)

st.markdown("---")
st.caption("💗 UMK Student Analytics | Pink Theme Dashboard")
