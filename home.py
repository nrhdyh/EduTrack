import streamlit as st
import pandas as pd

# ---------------------------------------
# CUSTOM CSS
# ---------------------------------------
st.markdown("""
<style>
body {
    background-color: #F7FAF7;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    text-align: center;
}

.card h3 {
    color: #2E7D32;
}

.card p {
    font-size: 18px;
}

.cta {
    background-color: #2E7D32;
    color: white;
    padding: 15px;
    border-radius: 12px;
    font-size: 18px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# HERO HEADER
# ---------------------------------------
st.markdown("""
<h1 style="text-align:center; color:#2E7D32;">🌱 Climate Smart Agriculture Survey</h1>
<p style="text-align:center; font-size:20px;">
Understanding <b>Education, Awareness & Practices</b> for Sustainable Farming
</p>
<hr>
""", unsafe_allow_html=True)

# ---------------------------------------
# QUICK INTRO CARDS
# ---------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>👤 Who?</h3>
        <p>Farmers, students & stakeholders</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📊 Why?</h3>
        <p>To analyze education & perception</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🌍 Impact</h3>
        <p>Support climate-smart agriculture</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------
# TABS
# ---------------------------------------
tab1, tab2 = st.tabs(["📝 Submit Survey", "📊 View Results"])

# ---------------------------------------
# TAB 1 — FORM
# ---------------------------------------
with tab1:
    st.markdown("""
    <div class="cta">
        📌 Your response takes less than <b>5 minutes</b> and helps real research
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.components.v1.iframe(
        "https://docs.google.com/forms/d/e/1FAIpQLSd9hFZX8_o6kSXONBgvT2O0xkzD8Vitltf3Hg3Q8nzguKs5YA/viewform?embedded=true",
        height=5000
    )

# ---------------------------------------
# TAB 2 — RESULTS
# ---------------------------------------
with tab2:
    st.subheader("📊 Live Survey Results")
    st.caption("Automatically updated from Google Forms")

    # Load data
    sheet_url = (
        "https://docs.google.com/spreadsheets/d/"
        "1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw/export?format=csv"
    )
    df = pd.read_csv(sheet_url)
    total_responses = len(df)

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("👥 Total Responses", total_responses)
    col2.metric("📋 Survey Questions", len(df.columns))
    col3.metric("🕒 Latest Entry", total_responses if total_responses > 0 else "-")

    st.progress(min(total_responses / 100, 1.0))
    st.caption("Survey progress indicator (target: 100 responses)")

    st.divider()

    # Dataset
    with st.expander("📄 View Full Dataset"):
        st.dataframe(df, use_container_width=True)

    # Column explorer
    st.write("### 🔎 Explore Individual Questions")
    selected_column = st.selectbox("Choose a question:", df.columns)
    st.dataframe(df[[selected_column]], use_container_width=True)

    # Download
    st.download_button(
        "⬇️ Download Dataset (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        "survey_data.csv",
        "text/csv"
    )
