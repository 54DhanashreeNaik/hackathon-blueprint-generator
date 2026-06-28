import streamlit as st

from src.utils.file_handlers import format_file_size


def show(app_state):

    docs = len(app_state.uploaded_files)

    size = sum(f.size_bytes for f in app_state.uploaded_files)

    completed = 1 if app_state.problem_analysis_results else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Documents",
            docs,
        )

    with col2:
        st.metric(
            "Storage",
            format_file_size(size),
        )

    with col3:
        st.metric(
            "Agents",
            f"{completed}/6",
        )