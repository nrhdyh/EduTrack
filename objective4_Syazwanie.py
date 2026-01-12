import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="EduTrack Academic Performance Dashboard",
    layout="wide"
)

# ---------------------------------------
# LOAD DATA
# ---------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nrhdyh/EduTrack/refs/heads/main/cleaned_student_performance_ver2.csv"
    return pd.read_csv(url)

df = load_data()

# ---------------------------------------
# STYLES
# ---------------------------------------
block_style = """
background: linear-gradient(135deg, #667eea, #764ba2);
color: white;
padding: 22px;
border-radius: 14px;
text-align: center;
box-shadow: 2px 4px 12px rgba(0,0,0,0.12);
"""

section_style = """
background: #f6f7fb;
padding: 22px;
border-radius: 14px;
"""

interpretation_style = """
background: linear-gradient(135deg, #f3e8ff, #ede9fe);
padding: 20px;
border-radius: 14px;
margin-top: 12px;
color: #2e1065;
box-shadow: 1px 3px 10px rgba(0,0,0,0.08);
"""

# ---------------------------------------
# TITLE & INTRODUCTION
# ---------------------------------------
st.title("🎓 EduTrack: The Impact of Skill Development and Co-curricular Engagement on Academic Performance")

st.markdown(f"""
<div style="{section_style}">
Student academic performance is a key indicator of higher education effectiveness.
Beyond GPA and CGPA, factors such as skill development and co-curricular engagement
play a significant role in shaping student success. This dashboard provides
visual analytics to explore how these factors influence academic outcomes among
Universiti Malaysia Kelantan (UMK) students.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------
# 📊 KEY SUMMARY INSIGHTS
# ---------------------------------------
st.subheader("📊 Key Summary Insights")

avg_gpa = df["GPA_Midpoint"].mean()
avg_cgpa = df["CGPA_Midpoint"].mean()
total_students = len(df)
active_rate = (df["Co_Curriculum_Activities_Text"] == "Yes").mean() * 100

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div style="{block_style}"><h5>Total Students</h5><h2>{total_students}</h2></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div style="{block_style}"><h5>Average GPA</h5><h2>{avg_gpa:.2f}</h2></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div style="{block_style}"><h5>Average CGPA</h5><h2>{avg_cgpa:.2f}</h2></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div style="{block_style}"><h5>Active Participation</h5><h2>{active_rate:.1f}%</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------
# 📄 DATASET PREVIEW (MATCH FRIEND STYLE)
# ---------------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df())
st.markdown("---")

# ---------------------------------------
# 🔍 DASHBOARD FILTERS
# ---------------------------------------
st.subheader("🔍 Dashboard Filters")

f1, f2, f3 = st.columns(3)

with f1:
    year = st.selectbox("Year of Study", ["All"] + sorted(df["Year_of_Study"].dropna().unique()))
with f2:
    skill = st.selectbox("Skill Development Level", ["All"] + sorted(df["Skill_Development_Hours_Category"].dropna().unique()))
with f3:
    cocur = st.selectbox("Co-Curricular Participation", ["All"] + sorted(df["Co_Curriculum_Activities_Text"].dropna().unique()))

filtered_df = df.copy()
if year != "All":
    filtered_df = filtered_df[filtered_df["Year_of_Study"] == year]
if skill != "All":
    filtered_df = filtered_df[filtered_df["Skill_Development_Hours_Category"] == skill]
if cocur != "All":
    filtered_df = filtered_df[filtered_df["Co_Curriculum_Activities_Text"] == cocur]

st.markdown("---")

# =====================================================
# 1️⃣ KDE – CGPA Density
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>1️⃣ CGPA Density: Active vs Non-Active Students</h3></div>', unsafe_allow_html=True)

active = filtered_df[filtered_df["Co_Curriculum_Activities_Text"] == "Yes"]["CGPA_Midpoint"].dropna()
inactive = filtered_df[filtered_df["Co_Curriculum_Activities_Text"] == "No"]["CGPA_Midpoint"].dropna()

fig1 = ff.create_distplot(
    [active, inactive],
    ["Active Students", "Non-Active Students"],
    show_hist=False,
    show_rug=False
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
st.dataframe(
    filtered_df.groupby("Co_Curriculum_Activities_Text")["CGPA_Midpoint"]
    .agg(["count", "mean", "std"]).round(2)
)

st.markdown(f"""
<div style="{interpretation_style}">
Active students show a tighter CGPA distribution with higher central values,
while non-active students exhibit wider variability, suggesting higher academic risk.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# 2️⃣ Grouped Bar – Average CGPA
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>2️⃣ Average CGPA by Skill Development & Co-Curricular</h3></div>', unsafe_allow_html=True)

grouped = filtered_df.groupby(
    ["Skill_Development_Hours_Category", "Co_Curriculum_Activities_Text"]
)["CGPA_Midpoint"].mean().reset_index()

fig2 = px.bar(
    grouped,
    x="Skill_Development_Hours_Category",
    y="CGPA_Midpoint",
    color="Co_Curriculum_Activities_Text",
    barmode="group"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
st.dataframe(grouped.round(2))

st.markdown("---")

# =====================================================
# 3️⃣ CGPA Distribution by Skills Category
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>3️⃣ CGPA Distribution by Skills Category</h3></div>', unsafe_allow_html=True)

cgpa_order = ["2.50 – 2.99", "3.00 – 3.69", "3.70 - 4.00"]

cross_tab = pd.crosstab(filtered_df["Skills_Category"], filtered_df["CGPA"])
cross_tab = cross_tab[[c for c in cgpa_order if c in cross_tab.columns]]

percentage = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
percentage = percentage.reset_index().melt(
    id_vars="Skills_Category",
    var_name="CGPA_Range",
    value_name="Percentage"
)

fig3 = px.bar(
    percentage,
    y="Skills_Category",
    x="Percentage",
    color="CGPA_Range",
    orientation="h",
    text=percentage["Percentage"].round(1)
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
st.dataframe(cross_tab)

st.markdown("---")

# =====================================================
# 4️⃣ Line Chart – CGPA Progression
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>4️⃣ CGPA Progression by Year & Skill Level</h3></div>', unsafe_allow_html=True)

line_data = filtered_df.groupby(
    ["Year_of_Study", "Skill_Development_Hours_Category"]
)["CGPA_Midpoint"].mean().reset_index()

fig4 = px.line(
    line_data,
    x="Year_of_Study",
    y="CGPA_Midpoint",
    color="Skill_Development_Hours_Category",
    markers=True
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
st.dataframe(line_data.round(2))

st.markdown("---")

# =====================================================
# 5️⃣ Heatmap – Average CGPA Matrix
# =====================================================
st.markdown(f'<div style="{block_style}"><h3>5️⃣ Average CGPA Heatmap</h3></div>', unsafe_allow_html=True)

heatmap_data = filtered_df.pivot_table(
    values="CGPA_Midpoint",
    index="Skill_Development_Hours_Category",
    columns="Co_Curriculum_Activities_Text",
    aggfunc="mean"
)

fig5 = px.imshow(
    heatmap_data,
    text_auto=".2f",
    aspect="auto"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("### 📊 Summary Statistics")
st.dataframe(heatmap_data.round(2))

st.markdown("---")

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.caption("🔵🟣 EduTrack Visual Analytics | Universiti Malaysia Kelantan")
