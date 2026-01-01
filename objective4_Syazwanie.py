import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="UMK Student Performance Dashboard",
    layout="wide"
)

st.title("📊 UMK Student Performance Analysis Dashboard")
st.markdown("""
This dashboard analyzes **UMK students' academic performance** based on  
**skill development**, **co-curricular participation**, and **study progression**.
""")

# ----------------------------------
# Load Dataset (GITHUB – NO FILE ERROR)
# ----------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/main/cleaned_student_performance.csv"
    return pd.read_csv(url)

df = load_data()

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("🔍 Filter Options")

year_filter = st.sidebar.multiselect(
    "Select Year of Study",
    sorted(df["Year_of_Study"].dropna().unique()),
    default=sorted(df["Year_of_Study"].dropna().unique())
)

skill_filter = st.sidebar.multiselect(
    "Select Skill Development Hours Category",
    df["Skill_Development_Hours_Category"].unique(),
    default=df["Skill_Development_Hours_Category"].unique()
)

df_filtered = df[
    df["Year_of_Study"].isin(year_filter) &
    df["Skill_Development_Hours_Category"].isin(skill_filter)
]

# ==================================
# 1️⃣ Performance Density
# ==================================
st.subheader("1️⃣ Performance Density: Active vs Non-Active Students")

fig_kde = px.histogram(
    df_filtered,
    x="CGPA_Midpoint",
    color="Co_Curriculum_Activities_Text",
    histnorm="probability density",
    nbins=30,
    opacity=0.6,
    marginal="rug"
)

st.plotly_chart(fig_kde, use_container_width=True)

# ==================================
# 2️⃣ Average CGPA
# ==================================
st.subheader("2️⃣ Average CGPA by Skill & Co-Curricular Activity")

df_grouped = (
    df_filtered
    .groupby(["Skill_Development_Hours_Category", "Co_Curriculum_Activities_Text"])
    ["CGPA_Midpoint"]
    .mean()
    .reset_index()
)

fig_bar = px.bar(
    df_grouped,
    x="Skill_Development_Hours_Category",
    y="CGPA_Midpoint",
    color="Co_Curriculum_Activities_Text",
    barmode="group"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ==================================
# 3️⃣ CGPA Percentage Distribution
# ==================================
st.subheader("3️⃣ CGPA Percentage Distribution by Skill Category")

cgpa_order = ["2.50 – 2.99", "3.00 – 3.69", "3.70 - 4.00"]

cross_tab = pd.crosstab(df_filtered["Skills_Category"], df_filtered["CGPA"])
cross_tab = cross_tab[[c for c in cgpa_order if c in cross_tab.columns]]

percentage = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage = percentage.reset_index().melt(
    id_vars="Skills_Category",
    var_name="CGPA Range",
    value_name="Percentage"
)

fig_stack = px.bar(
    percentage,
    y="Skills_Category",
    x="Percentage",
    color="CGPA Range",
    orientation="h",
    text="Percentage"
)

fig_stack.update_traces(texttemplate="%{text:.1f}%", textposition="inside")

st.plotly_chart(fig_stack, use_container_width=True)

# ==================================
# 4️⃣ Violin Plot
# ==================================
st.subheader("4️⃣ CGPA Distribution by Skill & Activity")

fig_violin = px.violin(
    df_filtered,
    x="Skill_Development_Hours_Category",
    y="CGPA_Midpoint",
    color="Co_Curriculum_Activities_Text",
    box=True,
    points="quartiles"
)

fig_violin.add_hline(
    y=df_filtered["CGPA_Midpoint"].mean(),
    line_dash="dash",
    line_color="red"
)

st.plotly_chart(fig_violin, use_container_width=True)

# ==================================
# 5️⃣ Academic Trend
# ==================================
st.subheader("5️⃣ Academic Progression Trend")

fig_line = px.line(
    df_filtered,
    x="Year_of_Study",
    y="CGPA_Midpoint",
    color="Skill_Development_Hours_Category",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.caption("© UMK | EduTrack Dashboard")
