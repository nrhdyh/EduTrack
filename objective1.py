import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Student Dashboard", layout="wide")

# ---------------------------
# Load Dataset
# ---------------------------
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTfh2K4-xu0yFkoRoOHxcEA4-CrRxZMNfe5EiflGI0OTLJUraozJV3Gp5sijGN8dVYyNOP29T5Fm39F/pub?gid=680023838&single=true&output=csv'
df = pd.read_csv(url)

st.title("📊 Student Demographic & Academic Dashboard")

# ---------------------------
# Gender Donut Chart
# ---------------------------
st.subheader("1️⃣ Gender Distribution Donut")

gender_counts = df["Gender"].value_counts()
labels = ["Female", "Male"]
fig = px.pie(
    values=gender_counts.values, 
    names=labels, 
    hole=0.6,
    color=labels,
    color_discrete_map={'Female':'pink','Male':'blue'}
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


# ---------------------------
# Avg GPA by Faculty
# ---------------------------
st.subheader("4️⃣ Average GPA by Faculty")
avg = df.groupby("Faculty")["GPA"].mean().reset_index()
fig = px.bar(avg, x="Faculty", y="GPA")
fig.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Avg GPA by Study Times
# ---------------------------
st.subheader("5️⃣ Average GPA by Study Time")
avgStudy = df.groupby("StudyTimes")["GPA"].mean().reset_index()
fig = px.bar(avgStudy, x="StudyTimes", y="GPA")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# GPA Category by Faculty × Gender
# ---------------------------
st.subheader("6️⃣ GPA Category – Stacked by Gender")

def categorize_gpa(x):
    if x < 2.5: return "Low"
    elif x <= 3.5: return "Medium"
    return "High"

df["GPA_Cat"] = df["GPA"].apply(categorize_gpa)
grouped = df.groupby(["Faculty","Gender","GPA_Cat"]).size().reset_index(name="Count")

fig = px.bar(
    grouped, 
    x="Faculty", y="Count",
    color="GPA_Cat", 
    barmode="stack", facet_col="Gender"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Bubble Chart – Age vs GPA
# ---------------------------
st.subheader("7️⃣ Age vs GPA Bubble (bubble = Study Hours)")
fig = px.scatter(df, x="Age", y="GPA", size="StudyHours", color="Gender", hover_data=["StudyHours"])
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Heatmap – Age Group × Study Hours
# ---------------------------
st.subheader("8️⃣ GPA Heatmap by Age Group × Study Hours")

df['Age_Group'] = pd.cut(df["Age"], bins=[18,20,22,24,26,28,30], labels=["18-19","20-21","22-23","24-25","26-27","28-29"])
df['SH_Group'] = pd.cut(df["StudyHours"], bins=[0,1,2,3,4,5,6,7], labels=["<1","1-2","2-3","3-4","4-5","5-6","6+"])
heat = df.groupby(["Age_Group","SH_Group"])["GPA"].mean().reset_index()

fig = px.imshow(
    heat.pivot(index="Age_Group", columns="SH_Group", values="GPA"),
    text_auto=True, aspect="auto", color_continuous_scale="RdBu"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Radar – Academic Metric
# ---------------------------
st.subheader("9️⃣ Radar Chart – Academic Performance by Gender")

metrics = ['GPA','CGPA','Attendance_Percentage','StudyHours','SocialMediaH','SkillHours']
mean_vals = df.groupby("Gender")[metrics].mean()

categories = metrics + [metrics[0]]
fig = go.Figure()

for g in mean_vals.index:
    values = mean_vals.loc[g].tolist()
    values.append(values[0])
    fig.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill='toself', name="Female" if g==0 else "Male"
    ))

fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# WordCloud Replacement – Text Frequency List
# ---------------------------
st.subheader("🔟 Skills WordCloud (Simple Text-Cloud Replacement)")

col1, col2 = st.columns(2)
female_skills = " ".join(df[df["Gender"]==0]["Skills"].dropna().astype(str)).split()
male_skills   = " ".join(df[df["Gender"]==1]["Skills"].dropna().astype(str)).split()

with col1:
    st.write("👩 Female Skills")
    st.write(pd.Series(female_skills).value_counts())

with col2:
    st.write("👨 Male Skills")
    st.write(pd.Series(male_skills).value_counts())
