import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Student Demographic Dashboard", layout="wide")

# =======================
# Load Dataset
# =======================
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTfh2K4-xu0yFkoRoOHxcEA4-CrRxZMNfe5EiflGI0OTLJUraozJV3Gp5sijGN8dVYyNOP29T5Fm39F/pub?gid=680023838&single=true&output=csv'
df = pd.read_csv(url)

st.title("📊 Student Demographic & Academic Dashboard")
st.write("Data Source:", url)

# =============================
# 1️⃣ Gender Donut Chart
# =============================
st.subheader("1️⃣ Distribution of Students by Gender")

gender_counts = df['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender','Count']
gender_counts['Gender'] = gender_counts['Gender'].map({0:'Female',1:'Male'})

fig = px.pie(
    gender_counts,
    names='Gender',
    values='Count',
    hole=0.5
)
st.plotly_chart(fig, use_container_width=True)

# =============================
# 2️⃣ Age Distribution by Gender (Bar Chart)
# =============================
st.subheader("2️⃣ Age Distribution by Gender")

pop = df.groupby(["Age","Gender"]).size().reset_index(name="Count")
pop['Gender'] = pop['Gender'].map({0:'Female',1:'Male'})

fig = px.bar(
    pop,
    x="Age",
    y="Count",
    color="Gender",
    barmode="group"
)

st.plotly_chart(fig, use_container_width=True)


# =============================
# GPA Distribution (Histogram)
# =============================
st.subheader("3️⃣ Distribution of GPA")

fig = px.histogram(
    df,
    x="GPA",
    nbins=10,
    marginal="box",   # replaces KDE insight
    title="Distribution of GPA"
)

fig.update_layout(
    xaxis_title="GPA",
    yaxis_title="Number of Students"
)

st.plotly_chart(fig, use_container_width=True)
True)

# =============================
# 4️⃣ Average GPA by Faculty
# =============================
st.subheader("4️⃣ Average GPA by Faculty")

avg_fac = df.groupby("Faculty")["GPA"].mean().reset_index()
fig = px.bar(avg_fac, x="Faculty", y="GPA")
st.plotly_chart(fig, use_container_width=True)

# =============================
# 5️⃣ Average GPA by Study Times
# =============================
st.subheader("5️⃣ Average GPA by Study Times")

avg_study = df.groupby("StudyTimes")["GPA"].mean().reset_index()
fig = px.bar(avg_study, x="StudyTimes", y="GPA")
st.plotly_chart(fig, use_container_width=True)

# =============================
# 6️⃣ GPA Category by Faculty & Gender
# =============================
st.subheader("6️⃣ GPA Category by Faculty & Gender")

def categorize_gpa(g):
    if g < 2.5:
        return "Low GPA"
    elif g <= 3.5:
        return "Medium GPA"
    return "High GPA"

df["GPA_Category"] = df["GPA"].apply(categorize_gpa)
df["Gender"] = df["Gender"].map({1:'Female',0:'Male'})

fig = px.histogram(
    df,
    x="Faculty",
    color="GPA_Category",
    facet_col="Gender",
    barmode="stack"
)
st.plotly_chart(fig, use_container_width=True)

# =============================
# 7️⃣ Bubble Chart – Age vs GPA
# =============================
st.subheader("7️⃣ Age vs GPA by Gender")

fig = px.scatter(
    df,
    x="Age",
    y="GPA",
    size="StudyHours",
    color="Gender"
)
st.plotly_chart(fig, use_container_width=True)

# # =============================
# # GPA Heatmap – Age Group x Study Hours
# # =============================
# st.subheader("8️⃣ Average GPA by Age Group & Study Hours")

# # Define bins
# age_bins = [18, 20, 22, 24, 26, 28, 30]
# age_labels = ['18-19', '20-21', '22-23', '24-25', '26-27', '28-29']
# df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

# study_bins = [0, 1, 2, 3, 4, 5, 6, 7]
# study_labels = ['<1', '1-2', '2-3', '3-4', '4-5', '5-6', '6+']
# df['StudyHours_Group'] = pd.cut(df['StudyHours'], bins=study_bins, labels=study_labels, right=False)

# # Calculate average GPA
# heatmap_df = (
#     df.groupby(['Age_Group','StudyHours_Group'])['GPA']
#       .mean()
#       .reset_index()
# )

# # Plot heatmap
# fig = px.density_heatmap(
#     heatmap_df,
#     x="StudyHours_Group",
#     y="Age_Group",
#     z="GPA",
#     text_auto=".2f",
#     color_continuous_scale="RdBu"
# )

# fig.update_layout(
#     xaxis_title="Study Hours Group",
#     yaxis_title="Age Group"
# )

# st.plotly_chart(fig, use_container_width=True)

# =============================
# 9️⃣ Radar Chart – Gender Metrics
# =============================
st.subheader("9️⃣ Academic & Engagement Radar")

metrics = ['GPA','CGPA','Attendance_Percentage','StudyHours','SocialMediaH','SkillHours']
means = df.groupby("Gender")[metrics].mean()

fig = go.Figure()

for gender in means.index:
    fig.add_trace(go.Scatterpolar(
        r=means.loc[gender],
        theta=metrics,
        fill='toself',
        name=gender
    ))

st.plotly_chart(fig, use_container_width=True)

# =============================
# 🔟 Violin Plot – GPA by Living
# =============================
st.subheader("🔟 GPA Distribution by Living Status")

fig = px.violin(df, x="Living", y="GPA", box=True)
st.plotly_chart(fig, use_container_width=True)

# =============================
# 1️⃣1️⃣ Skills Frequency by Gender
# =============================
st.subheader("1️⃣1️⃣ Skills Distribution by Gender")

skills = df[['Gender','Skills']].dropna()
skills['Skills'] = skills['Skills'].str.split(',')
skills = skills.explode('Skills')
skills['Skills'] = skills['Skills'].str.strip()

skill_count = skills.groupby(['Gender','Skills']).size().reset_index(name='Count')

fig = px.bar(
    skill_count,
    x="Skills",
    y="Count",
    color="Gender"
)
st.plotly_chart(fig, use_container_width=True)

st.success("🎉 Dashboard Render Complete (No Matplotlib Used)")
