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

st.markdown("### 📈 Variability Interpretation")
if st.checkbox("Show variability interpretation", value=True, key="desc3"):
    st.markdown("""
**What the graph shows:**  
The box plot displays the distribution and variability of CGPA across different learning modes, including Offline, Hybrid, and Online learning.

**Analysis:**  
The median CGPA remains relatively similar across all learning modes, indicating consistent overall performance. However, Offline learning shows a wider spread of CGPA values, suggesting greater variation in student performance. Hybrid and Online learning display more clustered results, with Hybrid learning showing the most consistent performance and fewer extreme values.

**Why this matters:**  
These results suggest that Hybrid learning offers a more stable and predictable environment for most students. Although Offline learning can lead to very high academic achievement for some students, its wider performance range may indicate uneven outcomes compared to the more consistent results seen in Hybrid learning.
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

st.markdown("### 📈 Yearly Preference Interpretation")
if st.checkbox("Show yearly interpretation", value=True, key="desc4"):
    st.markdown("""
**What the graph shows:**  
This stacked bar chart illustrates the distribution of learning mode preferences across different years of study at UMK.

**Analysis:**  
Year 1 students show a higher reliance on Offline and Hybrid learning as they establish their academic foundation and adapt to university life. As students progress to Year 3 and Year 4, there is a noticeable increase in preference for Hybrid learning. This likely reflects the need for greater flexibility to manage advanced coursework, final-year projects, and internships. Across all years, Online learning remains a smaller but consistent option.

**Why this matters:**  
These patterns highlight how students’ learning needs evolve over time. The findings suggest that hybrid learning models are particularly effective for senior students who require flexibility while still benefiting from structured academic support.
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

st.markdown("### 📈 Performance Risk Interpretation")
if st.checkbox("Show heatmap interpretation", value=True, key="desc5"):
    st.markdown("""
**What the graph shows:**  
This heatmap displays the average CGPA across different learning modes and years of study, with colour intensity representing performance levels.

**Analysis:**  
The highest academic performance is observed among Year 1 students in Offline learning, highlighting the importance of physical classroom engagement for new students. Year 2 students in Hybrid and Online learning also show strong academic performance. In contrast, Year 4 students in Online learning record the lowest average CGPA, indicating a potential decline in performance at higher academic levels when learning is fully online.

**Why this matters:**  
These findings point to potential academic risks for senior students in fully online learning environments. As academic demands increase, students may require more structured guidance and interaction, suggesting that hybrid or offline learning models may better support academic success in later years.
    """)

st.markdown("---")
st.caption("Developed for UMK Educational Analytics Dashboard.")
