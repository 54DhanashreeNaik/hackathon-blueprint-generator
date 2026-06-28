import streamlit as st


def show():
    st.title("🚀 Hackathon Blueprint Generator")

    st.markdown(
        """
Transform hackathon problem statements into **production-ready AI solution blueprints**
using an intelligent multi-agent workflow.

Upload your challenge documents, let AI analyze them, perform research,
validate technologies, and generate a complete implementation roadmap.
"""
    )

    st.info(
        "💡 Upload your hackathon documents to begin the AI-powered workflow."
    )