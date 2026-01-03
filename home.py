import streamlit as st
import pandas as pd
import base64

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(page_title="EDUTRACK UMK", layout="wide")

# ---------------------------------------
# BASE64 IMAGE LOADER
# ---------------------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("logo.png")

# ---------------------------------------
# HERO SECTION WITH LOGO (FIXED)
# ---------------------------------------
st.markdown(f"""
<style>
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.hero-box {{
    padding: 30px;
    text-align: center;
    background-color: #f8fbff;
    border-radius: 16px;
    animation: fadeInUp 1.2s ease-in-out;
}}

.hero-box img {{
    width: 300px;
    margin-bottom: 15px;
    background: white;
    padding: 12px;
    border-radius: 14px;
}}

.hero-box h1 {{
    color: #0d47a1;
    margin-bottom: 10px;
}}

.hero-box p {{
    font-size: 16px;
}}
</style>

<div class="hero-box">
    <img src="data:image/png;base64,{logo_base64}">
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

    sheet_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw/export?format=csv"
    )
    df = pd.read_csv(sheet_url)
    total_responses = len(df)

    st.markdown("### 🔢 Key Statistics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Students", total_responses)
    c2.metric("📋 Survey Items", len(df.columns))
    c3.metric("🎓 UMK Faculties", df.nunique().max())
    c4.metric("📅 Latest Response", "Live")

    st.progress(min(total_responses / 100, 1.0))
    st.caption("Progress: Target 100 UMK students")
