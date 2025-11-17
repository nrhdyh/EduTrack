import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------
# AUTO REFRESH (every 10 seconds)
# ---------------------------------------------------
st_autorefresh(interval=10000, key="auto_refresh")

# ---------------------------------------------------
# STREAMLIT PAGE SETTINGS
# ---------------------------------------------------
st.set_page_config(page_title="UMK Student Performance Dashboard",
                   layout="wide")

st.title("📊 UMK Student Performance Dashboard")
st.markdown("Real-time Google Form data — **NO API NEEDED**.")

# ---------------------------------------------------
# GOOGLE SHEET CSV LINK (YOUR SHEET)
# ---------------------------------------------------
CSV_URL = "https://docs.google.com/spreadsheets/d/1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw/edit?resourcekey=&gid=1949660483#gid=1949660483"

# ---------------------------------------------------
# LOAD DATA REAL-TIME
# ---------------------------------------------------
@st.cache_data(ttl=5)
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

try:
    df = load_data()
    st.success("✔ Successfully connected to Google Sheet (Live Data)")
except Exception as e:
    st.error("❌ Failed to load Google Sheet. Check sharing settings: Anyone with link → Viewer")
    st.write(e)
    st.stop()

# ---------------------------------------------------
# SHOW RAW DATA
# ---------------------------------------------------
st.header("📌 Google Form Responses (Live Table)")
st.dataframe(df, use_container_width=True)

# ---------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------
st.header("📊 Summary Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Submissions", len(df))

with col2:
    if "Gender" in df.columns:
        st.metric("Male Students", sum(df["Gender"] == "Male"))
    else:
        st.metric("Male Students", "-")

with col3:
    if "Gender" in df.columns:
        st.metric("Female Students", sum(df["Gender"] == "Female"))
    else:
        st.metric("Female Students", "-")

# ---------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------
st.header("📈 Visual Analytics")

# Pie Chart: Performance
if "Performance" in df.columns:
    fig1 = px.pie(df, names="Performance", title="Student Performance Breakdown")
    st.plotly_chart(fig1, use_container_width=True)

# Histogram: Program
if "Program" in df.columns:
    fig2 = px.histogram(df, x="Program", title="Students by Program")
    st.plotly_chart(fig2, use_container_width=True)

# Gender vs Performance
if "Gender" in df.columns and "Performance" in df.columns:
    fig3 = px.histogram(
        df,
        x="Performance",
        color="Gender",
        barmode="group",
        title="Performance by Gender"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# FILTER SECTION
# ---------------------------------------------------
st.header("🔍 Filter Data")

if "Program" in df.columns:
    program_list = ["All"] + sorted(df["Program"].unique().tolist())
    selected_program = st.selectbox("Select Program", program_list)
else:
    selected_program = "All"

filtered_df = df.copy()

if selected_program != "All":
    filtered_df = filtered_df[filtered_df["Program"] == selected_program]

st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Built for **UMK** • Google Forms → Google Sheets → Streamlit • Real-time Dashboard (No API)")
