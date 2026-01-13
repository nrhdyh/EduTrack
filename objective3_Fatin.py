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
# HELPER FUNCTION (From Friend's Style)
# ---------------------------------------
def sort_by_lower_bound(value):
    try:
        return float(value.split("-")[0].strip().replace("%", ""))
    except:
        return 0

#---------------------------------------
# TITLE & OVERVIEW
#---------------------------------------
st.title("🎓 Learning Mode Preference, Demographic Factors & Academic Outcomes Among UMK Students")
st.markdown("""
Learning mode preference plays an important role in shaping students’ learning experiences and academic outcomes. 
At Universiti Malaysia Kelantan (UMK), students adopt different learning modes including online, physical, and hybrid learning. 
These preferences may vary across demographic factors such as year of study and influence both short-term (GPA) and long-term (CGPA) academic performance.

This dashboard visually explores learning mode distribution, performance differences, variability, and year-based trends 
to support informed academic planning and decision-making.
""")
st.markdown("---")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance_ver2.csv"
df = pd.read_csv(url)

# =====================================================
# 📊 SUMMARY INSIGHT BLOCK BOXES
# =====================================================
st.subheader("📊 Key Summary Insights")

# Filters (Using Friend's Column Logic)
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    selected_year = st.selectbox(
        "Filter by Year of Study",
        ["All"] + sorted(df["Year_of_Study"].dropna().unique().tolist())
    )

with col_f2:
    selected_faculty = st.selectbox(
        "Filter by Faculty",
        ["All"] + sorted(df["Faculty_Short"].dropna().unique().tolist())
    )

with col_f3:
    selected_gender = st.selectbox(
        "Filter by Gender",
        ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    )

# Apply filters
filtered_df = df.copy()
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year_of_Study"] == selected_year]
if selected_faculty != "All":
    filtered_df = filtered_df[filtered_df["Faculty_Short"] == selected_faculty]
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

# Compute metrics for Objective 3
avg_gpa = filtered_df["GPA_Midpoint"].mean() if not filtered_df.empty else 0
dominant_mode = filtered_df["Learning_Mode"].mode()[0] if not filtered_df.empty else "N/A"
max_cgpa = filtered_df["CGPA_Midpoint"].max() if not filtered_df.empty else 0
total_count = len(filtered_df)

# Define the block style (Friend's Purple/Indigo Gradient)
block_style = """
    background: linear-gradient(135deg, #5E35B1, #3949AB);
    color:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
"""

# Display metrics in block boxes
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

# ---------------------------------------
# DATA PREVIEW
# ---------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())
st.markdown("---")

# =====================================================
# 1️⃣ Pie Chart: Learning Mode Distribution
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ Learning Mode Preference Distribution</h3></div>', unsafe_allow_html=True)

fig1 = px.pie(
    df, names='Learning_Mode', hole=0.4, 
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="Distribution of Preferred Learning Modes"
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 📌 Interpretation & Analysis")
if st.checkbox("Show interpretation", value=True, key="interpret1"):
    st.markdown("""
**What the graph shows:**  
The pie chart shows how UMK students prefer different learning modes, namely Hybrid, Offline, and Online learning.

**Analysis:**  
The results indicate that Hybrid learning is the most preferred mode, with more than half of the students selecting this option. This suggests that students value the flexibility of online components while still appreciating face-to-face interaction. Offline learning remains the second most preferred mode, indicating that traditional classroom learning is still important. In contrast, Online learning is the least preferred option, showing that fully remote learning is less favoured among students.

**Why this matters:**  
These findings highlight students’ preference for a balanced learning approach rather than fully online or fully physical modes. This insight is important for academic planning, as it suggests that hybrid learning should be prioritised to better align with students’ learning needs and preferences.
    """)

st.markdown("---")

# =====================================================
# 2️⃣ Bar Chart: Average GPA by Learning Mode (UPDATED)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Bar Chart: Average GPA by Learning Mode</h3></div>', unsafe_allow_html=True)

# Calculation for GPA instead of CGPA
avg_gpa_data = df.groupby('Learning_Mode')['GPA_Midpoint'].mean().reset_index()

fig2 = px.bar(
    avg_gpa_data, x='Learning_Mode', y='GPA_Midpoint', 
    text_auto='.2f', 
    color_discrete_sequence=px.colors.sequential.Viridis,
    title="Comparison of Mean GPA Across Learning Modes"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
if st.checkbox("Show performance stats", value=True, key="stats2"):
    st.dataframe(avg_gpa_data, use_container_width=True)

st.markdown("### 📈 Performance Interpretation")
if st.checkbox("Show performance interpretation", value=True, key="desc2"):
    st.markdown("""
**What the graph shows:**  
The bar chart compares the average GPA of UMK students across different learning modes, namely Offline, Hybrid, and Online learning.

**Analysis:**  
The results indicate that the average GPA is very similar across all learning modes, remaining around 3.4. Offline learning shows a slightly higher average GPA, which may be due to direct interaction with lecturers and peers. However, the differences are minimal, suggesting that students can achieve comparable academic performance regardless of the learning mode.

**Why this matters:**  
This finding shows that learning mode alone does not significantly influence academic performance. It highlights students’ adaptability and supports the use of flexible learning approaches, such as hybrid learning, without negatively affecting academic outcomes.
    """)

st.markdown("---")

# =====================================================
# 3️⃣ Box Plot: CGPA Variability
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ Box Plot: CGPA Distribution by Learning Mode</h3></div>', unsafe_allow_html=True)

fig3 = px.box(
    df, x='Learning_Mode', y='CGPA_Midpoint',
    color_discrete_sequence=px.colors.sequential.Viridis,
    title="CGPA Variability and Spread per Learning Mode"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
if st.checkbox("Show variability stats", value=True, key="stats3"):
    variability_stats = df.groupby("Learning_Mode")["CGPA_Midpoint"].agg(["min", "median", "max", "std"]).reset_index()
    st.dataframe(variability_stats, use_container_width=True)

st.markdown("### 📈 Distribution Description")
if st.checkbox("Show variability description", value=True, key="desc3"):
    st.markdown("""
The box plot provides deeper insight into the variability of student performance. While the median CGPA remains relatively stable across all groups, the Offline mode displays the greatest variance, represented by a much larger box and longer whiskers. This indicates that while Offline learning can lead to exceptionally high scores, it also carries a wider range of performance outcomes compared to the more "clustered" results seen in the Hybrid and Online groups. The Hybrid mode shows the most consistency, with fewer extremes, suggesting it provides a reliable and predictable environment for the majority of students to maintain their grades.
    """)

st.markdown("---")

# =====================================================
# 4️⃣ Stacked Bar: Mode by Year (Dropdown Filter)
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ Stacked Bar: Mode Preference by Year of Study</h3></div>', unsafe_allow_html=True)

# Using Friend's Dropdown Pattern
year_opts = sorted(df["Year_of_Study"].dropna().unique())
selected_year_chart = st.selectbox("Select Year of Study to Focus", ["All"] + list(year_opts))

chart_df = df if selected_year_chart == "All" else df[df["Year_of_Study"] == selected_year_chart]

fig4 = px.histogram(
    chart_df, x='Year_of_Study', color='Learning_Mode', 
    barmode='stack', color_discrete_sequence=px.colors.qualitative.Set2,
    title=f"Learning Mode Distribution: {selected_year_chart}"
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("### 📈 Distribution Description")
if st.checkbox("Show yearly description", value=True, key="desc4"):
    st.markdown("""
This visualization highlights a clear shift in student needs as they progress through their academic journey. Year 1 students show a relatively higher reliance on Offline and Hybrid modes as they establish their academic foundation. As students reach Year 3 and Year 4, there is a massive surge in the total number of students preferring Hybrid learning. This trend likely reflects senior students' need for greater schedule flexibility to balance advanced coursework, final-year projects, or internships. Notably, the preference for purely Online learning remains a small but consistent niche across all four years.
    """)

st.markdown("---")

# =====================================================
# 5️⃣ Heatmap: Success Matrix
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ Heatmap: Average CGPA Success Matrix</h3></div>', unsafe_allow_html=True)

heatmap_data = df.groupby(['Learning_Mode', 'Year_of_Study'])['CGPA_Midpoint'].mean().reset_index()

fig5 = px.density_heatmap(
    heatmap_data, x='Year_of_Study', y='Learning_Mode', z='CGPA_Midpoint',
    text_auto=".2f", color_continuous_scale="Viridis",
    labels={'CGPA_Midpoint': 'Avg CGPA'},
    title="Success Matrix: Year vs. Mode"
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
if st.checkbox("Show heatmap stats", value=True, key="stats5"):
    st.dataframe(heatmap_data, use_container_width=True)

st.markdown("### 📈 Distribution Description")
if st.checkbox("Show heatmap description", value=True, key="desc5"):
    st.markdown("""
The heatmap identifies specific "performance corridors" where students excel most. The highest academic density is found among Year 1 Offline students (3.72), reinforcing the idea that physical presence is crucial for new students adapting to university standards. Another high-performing segment is Year 2 Hybrid and Online students, both averaging 3.68. However, a significant academic risk is identified in Year 4 Online students, where the average CGPA drops to its lowest point of 3.04. This suggests that senior-level complexity may require more direct supervision than a fully online environment can provide.
    """)

st.markdown("---")
st.caption("Developed for UMK Educational Analytics Dashboard.")
