import streamlit as st

st.set_page_config(
    page_title="EduTrack Dashboard",
    layout="wide"
)

# Pages
home = st.Page(
    "home.py",
    title="🏠 Home",
    default=True
)

# objective1 = st.Page(
#     "objective1.py",
#     title="👤 Demographics"
# )

# objective2 = st.Page(
#     "objective2.py",
#     title="📚 Study & Lifestyle"
# )

# objective3 = st.Page(
#     "objective3.py",
#     title="💻 Learning Mode"
# )

# objective4 = st.Page(
#     "objective4.py",
#     title="🛠️ Skills & Activities"
# )

# Navigation
pg = st.navigation(
    {
        "📌 Dashboard Sections": [
            home
            # objective1,
            # objective2,
            # objective3,
            # objective4
        ]
    }
)

pg.run()

