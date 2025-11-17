import streamlit as st
import pandas as pd

st.set_page_config(page_title="Survey Dashboard", layout="wide")

# ---------------------------------------
# HEADER
# ---------------------------------------
st.markdown("""
    <h1 style='text-align:center; color:#2E7D32;'>📋 Survey Dashboard</h1>
    <p style='text-align:center; font-size:18px;'>Submit your response and view real-time results instantly</p>
    <br>
""", unsafe_allow_html=True)

# Tabs for navigation
tab1, tab2 = st.tabs(["📝 Submit Response", "📊 Live Results"])

# ---------------------------------------
# TAB 1 — Submit Form
# ---------------------------------------
with tab1:
    st.subheader("✏️ Submit Your Survey Form")
    st.info("Please fill in the survey below. Your responses update the dashboard automatically.")

    st.components.v1.iframe(
        "https://docs.google.com/forms/d/e/1FAIpQLSd9hFZX8_o6kSXONBgvT2O0xkzD8Vitltf3Hg3Q8nzguKs5YA/viewform?embedded=true",
        height=5000
    )

# ---------------------------------------
# TAB 2 — Live Results
# ---------------------------------------
with tab2:
    st.subheader("📊 Real-Time Survey Data")
    st.caption("Data auto-refreshes whenever the app reloads.")

    # Load data
    sheet_url = "https://docs.google.com/spreadsheets/d/1IVXi1nQYuM_tQolHWv6asvttHkbDRWpSW20VuSptEvw/export?format=csv"
    df = pd.read_csv(sheet_url)

    # Summary Section
    total_responses = len(df)

    st.write("### 📈 Overview")

    # Custom metric-style cards using only HTML (compatible with Streamlit Cloud)
    card_html = """
       <div style="
    background-color: #2E7D32;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
">
    <h3>{title}</h3>
    <p style="font-size:30px; font-weight:bold; margin-top:-10px;">{value}</p>
</div>

    """

    col1, col2, col3 = st.columns(3)

    col1.markdown(card_html.format(title="Total Responses", value=total_responses), unsafe_allow_html=True)
    col2.markdown(card_html.format(title="Columns", value=len(df.columns)), unsafe_allow_html=True)
    col3.markdown(card_html.format(title="Latest Entry Row", value=total_responses if total_responses > 0 else "-"), unsafe_allow_html=True)

    st.write("---")

    # Expandable raw data
    with st.expander("📄 View Full Dataset"):
        st.dataframe(df, use_container_width=True)

    st.write("---")

    # Quick Filters
    st.write("### 🎛️ Filter Options")
    selected_column = st.selectbox("Select a column to explore:", df.columns)
    st.dataframe(df[[selected_column]])

    # Download button
    st.download_button(
        "⬇️ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "survey_data.csv",
        "text/csv",
        help="Download the full dataset",
    )
