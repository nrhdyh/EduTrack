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
st.markdown(
    """
    This dashboard analyzes **UMK students' academic performance** based on  
    **skill development**, **co-curricular participation**, and **study progression**.
    """
)

# ----------------------------------
# Load Dataset
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("processed_data.csv")

df = load_data()

# ----------------------------------
# Sidebar Filters
# ----------------------------------
st.sidebar.header("🔍 Filter Options")

year_filter = st.sidebar.multiselect(
    "Select Year of Study",
    options=sorted(df["Year_of_Study"].dropna().unique()),
    default=sorted(df["Year_of_Study"].dropna().unique())
)

skill_filter = st.sidebar.multiselect(
    "Select Skill Development Hours Category",
    options=df["Skill_Development_Hours_Category"].unique(),
    default=df["Skill_Development_Hours_Category"].unique()
)

df_filtered = df[
    (df["Year_of_Study"].isin(year_filter)) &
    (df["Skill_Development_Hours_Category"].isin(skill_filter))
]

# ==================================
# 1️⃣ Performance Density (KDE-like)
# ==================================
st.subheader("1️⃣ Performance Density: Active vs Non-Active Students")

fig_kde = px.histogram(
    df_filtered,
    x="CGPA_Midpoint",
    color="Co_Curriculum_Activities_Text",
    histnorm="probability density",
    nbins=30,
    opacity=0.6,
    marginal="rug",
    title="Performance Density Distribution"
)

fig_kde.update_layout(
    xaxis_title="CGPA Midpoint",
    yaxis_title="Density"
)

st.plotly_chart(fig_kde, use_container_width=True)

# ==================================
# 2️⃣ Average CGPA by Skill & Activity
# ==================================
st.subheader("2️⃣ Average CGPA by Skill Development & Co-Curricular Participation")

df_grouped = (
    df_filtered.groupby(
        ["Skill_Development_Hours_Category", "Co_Curriculum_Activities_Text"]
    )["CGPA_Midpoint"]
    .mean()
    .reset_index()
)

fig_bar = px.bar(
    df_grouped,
    x="Skill_Development_Hours_Category",
    y="CGPA_Midpoint",
    color="Co_Curriculum_Activities_Text",
    barmode="group",
    title="Average CGPA by Skill Development Level",
    labels={
        "Skill_Development_Hours_Category": "Skill Development Hours",
        "CGPA_Midpoint": "Average CGPA"
    }
)

st.plotly_chart(fig_bar, use_container_width=True)

# ==================================
# 3️⃣ CGPA Percentage Distribution
# ==================================
st.subheader("3️⃣ Percentage Distribution of CGPA by Skill Category")

cgpa_order = ["2.50 – 2.99", "3.00 – 3.69", "3.70 - 4.00"]

cross_tab = pd.crosstab(
    df_filtered["Skills_Category"],
    df_filtered["CGPA"]
)

available_order = [c for c in cgpa_order if c in cross_tab.columns]
cross_tab = cross_tab[available_order]

percentage_dist = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage_dist = percentage_dist.reset_index()

percentage_melted = percentage_dist.melt(
    id_vars="Skills_Category",
    value_vars=available_order,
    var_name="CGPA Range",
    value_name="Percentage"
)

fig_stack = px.bar(
    percentage_melted,
    y="Skills_Category",
    x="Percentage",
    color="CGPA Range",
    orientation="h",
    title="CGPA Percentage Distribution by Skill Category",
    text="Percentage"
)

fig_stack.update_layout(
    xaxis=dict(range=[0, 100]),
    xaxis_title="Percentage of Students (%)",
    yaxis_title="Skills Category"
)

fig_stack.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="inside"
)

st.plotly_chart(fig_stack, use_container_width=True)

# ==================================
# 4️⃣ CGPA Distribution (Violin Plot)
# ==================================
st.subheader("4️⃣ CGPA Distribution by Skill Development & Activity")

fig_violin = px.violin(
    df_filtered,
    x="Skill_Development_Hours_Category",
    y="CGPA_Midpoint",
    color="Co_Curriculum_Activities_Text",
    box=True,
    points="quartiles",
    title="CGPA Distribution by Skill Development Level"
)

fig_violin.add_hline(
    y=df_filtered["CGPA_Midpoint"].mean(),
    line_dash="dash",
    line_color="red",
    annotation_text="Overall Average CGPA",
    annotation_position="top left"
)

st.plotly_chart(fig_violin, use_container_width=True)

# ==================================
# 5️⃣ Academic Progression Trend
# ==================================
st.subheader("5️⃣ Academic Progression: CGPA Trend Over Years")

fig_line = px.line(
    df_filtered,
    x="Year_of_Study",
    y="CGPA_Midpoint",
    color="Skill_Development_Hours_Category",
    markers=True,
    title="CGPA Trends by Year of Study & Skill Development Level"
)

fig_line.update_layout(
    xaxis_title="Year of Study",
    yaxis_title="CGPA Midpoint"
)

st.plotly_chart(fig_line, use_container_width=True)

# ----------------------------------
# Footer
# ----------------------------------
st.markdown("---")
st.caption("© UMK | Student Academic Performance Analysis Dashboard")
