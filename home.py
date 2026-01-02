import streamlit as st
import pandas as pd

# ---------------------------------------
# CUSTOM CSS (UMK THEME)
# ---------------------------------------
st.markdown("""
<style>
body {
    background-color: #F6F4FA;
}

.hero {
    background: linear-gradient(135deg, #5E35B1, #3949AB);
    padding: 40px;
    border-radius: 20px;
    color: white;
    text-align: center;
}

.hero h1 {
    font-size: 42px;
}

.hero p {
    font-size: 20px;
    opacity: 0.95;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.08);
    text-align: center;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-6px);
}

.card h3 {
    color: #5E35B1;
}

.cta {
    background-color: #5E35B1;
    color: white;
    padding: 18px;
    border-radius: 14px;
    font-size: 18px;
    text-align: center;
}

.section-title {
    color: #3949AB;
    font-size: 26px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# HERO SECTION WITH LOGO
# ---------------------------------------
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.image("logo.png", width=500)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="hero" style="padding:20px; text-align:center;">
    <h1>🎓 EDUTRACK UMK</h1>
    <p>
        Understanding <b>Students’ Demographics, Learning Behaviour & Skills</b><br>
        Universiti Malaysia Kelantan
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------
# TABS
# ---------------------------------------
tab1, tab2 = st.tabs(["📝 Participate in Survey", "📊 Explore Results"])

# ---------------------------------------
# TAB 1 — SURVEY FORM
# ---------------------------------------
with tab1:
    st.markdown("""
    <div class="cta">
        💜 Your voice matters! <b>Help UMK improve student learning experience</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.components.v1.iframe(
        "https://docs.google.com/forms/d/e/1FAIpQLSd9hFZX8_o6kSXONBgvT2O0xkzD8Vitltf3Hg3Q8nzguKs5YA/viewform?embedded=true",
        height=5000
    )

# ---------------------------------------
# TAB 2 — LIVE RESULTS + ANALYTICS
# ---------------------------------------
with tab2:
    st.markdown('<h2 class="section-title">📊 Homepage Analytics Overview</h2>', unsafe_allow_html=True)
    st.caption("Automatically updated from Google Forms")

    # Load Google Sheets CSV
    sheet_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw/export?format=csv"
    )
    df = pd.read_csv(sheet_url)
    total_responses = len(df)

    # ---------------------------------------
    # KPI METRICS
    # ---------------------------------------
    st.markdown("### 🔢 Key Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Total Students", total_responses)
    col2.metric("📋 Survey Items", len(df.columns))

    if "Faculty" in df.columns:
        faculties_count = (
            df["Faculty"]
            .astype(str)
            .str.strip()
            .replace("nan", None)
            .dropna()
            .nunique()
        )
    elif "Faculty_Short" in df.columns:
        faculties_count = (
            df["Faculty_Short"]
            .astype(str)
            .str.strip()
            .replace("nan", None)
            .dropna()
            .nunique()
        )
    else:
        faculties_count = "-"

    col3.metric("🎓 UMK Faculties", faculties_count)
    col4.metric("📅 Latest Response", "Live")

    st.progress(min(total_responses / 100, 1.0))
    st.caption("Progress: Target 100 UMK students")

    st.divider()

    # ---------------------------------------
    # DEMOGRAPHICS SNAPSHOT
    # ---------------------------------------
    st.markdown("### 👤 Demographics Snapshot")
    demo_col = st.selectbox(
        "Select a demographic variable:",
        df.columns[2:5]
    )
    demo_counts = df[demo_col].value_counts()
    st.bar_chart(demo_counts)
    st.caption(f"Distribution of UMK students by **{demo_col}**")

    st.divider()

    # ---------------------------------------
    # STUDY & LEARNING TREND
    # ---------------------------------------
    st.markdown("### 📚 Study & Learning Trends")
    trend_col = st.selectbox(
        "Select a learning-related question:",
        df.columns[5:10] if len(df.columns) > 10 else df.columns
    )
    trend_counts = df[trend_col].value_counts()
    st.line_chart(trend_counts)
    st.caption(f"Trend analysis for **{trend_col}**")

    st.divider()

    # ---------------------------------------
    # QUICK INSIGHTS
    # ---------------------------------------
    st.markdown("### 💡 Quick Insights")
    most_common_demo = demo_counts.idxmax()
    most_common_demo_value = demo_counts.max()

    st.success(
        f"Most UMK students selected **{most_common_demo}** for **{demo_col}** "
        f"({most_common_demo_value} responses)."
    )

    st.info(
        "Students show diverse learning patterns. "
        "Detailed breakdowns are available in each objective section."
    )

    st.divider()

    # ---------------------------------------
    # DATA EXPLORER
    # ---------------------------------------
    with st.expander("📄 View Full Dataset"):
        st.dataframe(df, use_container_width=True)

    st.markdown("### 🔍 Explore by Question")
    selected_column = st.selectbox("Choose a question:", df.columns)
    st.dataframe(df[[selected_column]], use_container_width=True)

    st.download_button(
        "⬇️ Download Data (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        "edutrack_umk_data.csv",
        "text/csv"
    )

    st.markdown("""
    <div class="cta">
    👉 Use the sidebar to navigate <b>Demographics, Study & Lifestyle, Learning Mode,</b>
    and <b>Skills & Activities</b> for detailed insights
    </div>
    """, unsafe_allow_html=True)
