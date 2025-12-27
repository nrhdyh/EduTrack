import streamlit as st
import pandas as pd

# ---------------------------------------
# CUSTOM CSS (UMK THEME)
# ---------------------------------------
st.markdown("""
<style>
body {


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
# HERO SECTION
# ---------------------------------------
st.markdown("""
<div class="hero">
    <h1>🎓 EDUTRACK UMK</h1>
    <p>
        Understanding <b>Students’ Demographics, Learning Behaviour & Skills</b><br>
        Universiti Malaysia Kelantan
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------
# OVERVIEW CARDS
# ---------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <h3>👤 Demographics</h3>
        <p>Student background & profile</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📚 Study & Lifestyle</h3>
        <p>Study habits & daily routines</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>💻 Learning Mode</h3>
        <p>Online & physical learning styles</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <h3>🛠️ Skills & Activities</h3>
        <p>Co-curricular & personal skills</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------
# TABS
# ---------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
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
# TAB 2 — LIVE RESULTS
# ---------------------------------------
with tab2:
    st.markdown('<h2 class="section-title">📊 Live Student Responses</h2>', unsafe_allow_html=True)
    st.caption("Data updates automatically from Google Forms")

    sheet_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw/export?format=csv"
    )
    df = pd.read_csv(sheet_url)

    total_responses = len(df)

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Students", total_responses)
    col2.metric("📋 Survey Questions", len(df.columns))
    col3.metric("🎓 UMK Participation", f"{min(total_responses,100)}%")

    st.progress(min(total_responses / 100, 1.0))
    st.caption("Target: 100 UMK students")

    st.divider()

    # Data viewer
    with st.expander("📄 View Raw Responses"):
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
