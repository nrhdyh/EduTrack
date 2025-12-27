# ==========================================
# 1. IMPORT LIBRARIES
# ==========================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 2. LOAD DATA FROM GOOGLE SHEET
# ==========================================
sheet_id = "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw"
sheet_name = "cleaned_data"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

df = pd.read_csv(url)

print("Data Loaded Successfully")
print(df.head())

# ==========================================
# 3. DATA CLEANING
# ==========================================
# Convert relevant columns to numeric
df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
df['Attendance'] = pd.to_numeric(df['Attendance'], errors='coerce')
df['YearStudy'] = pd.to_numeric(df['YearStudy'], errors='coerce')

# Drop rows with missing GPA
df = df.dropna(subset=['GPA'])

# ==========================================
# 4. VISUALIZATION SETTINGS
# ==========================================
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (8,5)

# ==========================================
# 5. VISUALIZATIONS
# ==========================================

# 1️⃣ Bar Chart – Average GPA by Gender
plt.figure()
sns.barplot(x='Gender', y='GPA', data=df, ci=None)
plt.title("Average GPA by Gender")
plt.ylabel("Average GPA")
plt.xlabel("Gender")
plt.show()


# 2️⃣ Box Plot – GPA Distribution by Year of Study
plt.figure()
sns.boxplot(x='YearStudy', y='GPA', data=df)
plt.title("GPA Distribution by Year of Study")
plt.xlabel("Year of Study")
plt.ylabel("GPA")
plt.show()


# 3️⃣ Grouped Bar Chart – Average GPA by Faculty
plt.figure(figsize=(10,5))
faculty_order = df.groupby('Faculty')['GPA'].mean().sort_values(ascending=False).index
sns.barplot(x='Faculty', y='GPA', data=df, order=faculty_order, ci=None)
plt.title("Average GPA by Faculty")
plt.xlabel("Faculty")
plt.ylabel("Average GPA")
plt.xticks(rotation=45, ha='right')
plt.show()


# 4️⃣ Scatter Plot – Attendance Percentage vs GPA
plt.figure()
sns.scatterplot(x='Attendance', y='GPA', hue='YearStudy', data=df)
plt.title("Attendance Percentage vs GPA")
plt.xlabel("Attendance (%)")
plt.ylabel("GPA")
plt.show()


# 5️⃣ Box Plot – Scholarship Status vs GPA
plt.figure()
sns.boxplot(x='Scholarship', y='GPA', data=df)
plt.title("Scholarship Status vs GPA")
plt.xlabel("Scholarship Status")
plt.ylabel("GPA")
plt.show()


# 6️⃣ Heatmap – Year of Study × Faculty vs GPA
pivot_table = df.pivot_table(
    values='GPA',
    index='YearStudy',
    columns='Faculty',
    aggfunc='mean'
)

plt.figure(figsize=(12,6))
sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="YlGnBu")
plt.title("Heatmap: Year of Study × Faculty vs Average GPA")
plt.xlabel("Faculty")
plt.ylabel("Year of Study")
plt.show()


# 7️⃣ Line Chart – GPA Trend Across Years of Study
yearly_gpa = df.groupby('YearStudy')['GPA'].mean().reset_index()

plt.figure()
sns.lineplot(x='YearStudy', y='GPA', data=yearly_gpa, marker='o')
plt.title("GPA Trend Across Years of Study")
plt.xlabel("Year of Study")
plt.ylabel("Average GPA")
plt.show()

# ==========================================
# END OF SCRIPT
# ==========================================
