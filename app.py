import streamlit as st
from pathlib import Path
from src.models.state import AppState
from src.views import home, problem_analysis, research, evidence, intelligence, blueprint, export

# 1. Page Configuration
st.set_page_config(
    page_title="Hackathon Blueprint Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS Style
css_path = Path(__file__).parent / "assets" / "custom.css"
if css_path.exists():
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Session State Initialization
if "app_state" not in st.session_state:
    st.session_state.app_state = AppState()

# 4. Multi-Page Navigation Configuration
pg = st.navigation({
    "Navigate": [
        st.Page(home.show, title="Home", icon="🏠"),
        st.Page(problem_analysis.show, title="Problem Analysis", icon="🔍"),
        st.Page(research.show, title="Research", icon="🌐"),
        st.Page(evidence.show, title="Evidence", icon="📊"),
        st.Page(intelligence.show, title="Intelligence", icon="🧠"),
        st.Page(blueprint.show, title="Blueprint", icon="🗺️"),
        st.Page(export.show, title="Export", icon="📤")
    ]
})

# 5. Run Navigation Router
pg.run()
