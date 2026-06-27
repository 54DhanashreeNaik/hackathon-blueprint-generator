import streamlit as st
from pathlib import Path

from src.models.state import AppState
from src.views import (
    home,
    problem_analysis,
    research,
    evidence,
    intelligence,
    blueprint,
    export,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Hackathon Blueprint Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Load Custom CSS
# --------------------------------------------------
css_path = Path(__file__).parent / "assets" / "custom.css"

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# Initialize Global App State
# --------------------------------------------------
if "app_state" not in st.session_state:
    st.session_state.app_state = AppState()

# --------------------------------------------------
# Navigation
# --------------------------------------------------
pages = [
    st.Page(home.show, title="Home", icon="🏠", url_path="home"),
    st.Page(problem_analysis.show, title="Problem Analysis", icon="🔍", url_path="problem-analysis"),
    st.Page(research.show, title="Research", icon="🌐", url_path="research"),
    st.Page(evidence.show, title="Evidence", icon="📊", url_path="evidence"),
    st.Page(intelligence.show, title="Intelligence", icon="🧠", url_path="intelligence"),
    st.Page(blueprint.show, title="Blueprint", icon="🗺️", url_path="blueprint"),
    st.Page(export.show, title="Export", icon="📤", url_path="export"),
]

pg = st.navigation(pages)

# --------------------------------------------------
# Run Selected Page
# --------------------------------------------------
pg.run()