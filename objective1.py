# objective1.py
# Objective 1: Demographics & Academic Factors Visualizations (Live Google Sheet)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Step 1: Load Google Sheet directly
# -----------------------------
# Replace your sheet ID and gid
sheet_id = "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw"
gid = "680023838"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

df = pd.read_csv(url)
print(df.head())

# -----------------------------
# Step 2: Data Cleaning
# -----------------------------
# Ensure GPA is numeric
def convert_gpa(value):
    if pd.isna(value):
        return None
    if "–" in str(value):
        low, high = value.split("–")
        return (float(low.strip()) + float(high.strip())) / 2
    try:
        return float(value)
    except:
        return None

df["GPA"] = df["GPA"].apply(convert_gpa)

# Ensure Attendance is numeric if stored as string %
if df["Attendance"].dtype == object:
    df["Attendance"] = df["Attendance"].str.replace("%", "").astype(float)

# -----------------------------
# Step 3: Visualizations
# -----------------------------
sns.set(style="whitegrid")

# 1️⃣ Bar Chart – Average GPA by Gender
plt.figure(figsize=(6,5))
avg_gpa_gender = df.groupby("Gender")["GPA"].mean().reset_index()
sns.barplot(data=avg_gpa_gender, x="Gender", y="GPA", palette="pastel")
plt.title("Average GPA by Gender")
plt.ylabel("Average GPA")
plt.savefig("avg_gpa_by_gender.png")
plt.show()

# 2️⃣ Box Plot – GPA distribution by Year of Study
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x="YearStudy", y="GPA", palette="Set2")
plt.title("GPA Distribution by Year of Study")
plt.savefig("gpa_by_year.png")
plt.show()

# 3️⃣ Grouped Bar Chart – Average GPA by Faculty
plt.figure(figsize=(10,5))
avg_gpa_faculty = df.groupby("Faculty")["GPA"].mean().reset_index()
sns.barplot(data=avg_gpa_faculty, x="Faculty", y="GPA", palette="muted")
plt.xticks(rotation=45)
plt.title("Average GPA by Faculty")
plt.savefig("avg_gpa_by_faculty.png")
plt.show()

# 4️⃣ Scatter Plot – Attendance % vs GPA
plt.figure(figsize=(6,5))
sns.scatterplot(data=df, x="Attendance", y="GPA", hue="YearStudy", palette="deep")
plt.title("Attendance Percentage vs GPA")
plt.savefig("attendance_vs_gpa.png")
plt.show()

# 5️⃣ Box Plot – Scholarship Status vs GPA
plt.figure(figsize=(6,5))
sns.boxplot(data=df, x="Scholarship", y="GPA", palette="Set3")
plt.title("Scholarship Status vs GPA")
plt.savefig("scholarship_vs_gpa.png")
plt.show()

# 6️⃣ Heatmap – Year of Study × Faculty vs GPA
plt.figure(figsize=(10,6))
pivot_table = df.pivot_table(index="YearStudy", columns="Faculty", values="GPA", aggfunc="mean")
sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="YlGnBu")
plt.title("Heatmap: Year × Faculty vs GPA")
plt.savefig("heatmap_year_faculty_gpa.png")
plt.show()

# 7️⃣ Line Chart – GPA Trend Across Years of Study
plt.figure(figsize=(6,5))
gpa_trend = df.groupby("YearStudy")["GPA"].mean().reset_index()
sns.lineplot(data=gpa_trend, x="YearStudy", y="GPA", marker="o", color="purple")
plt.title("GPA Trend Across Years of Study")
plt.savefig("gpa_trend_years.png")
plt.show()

print("All visualizations generated from live Google Sheet data.")

