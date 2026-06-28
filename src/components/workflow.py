import streamlit as st


def show(app_state):

    st.subheader("Workflow")

    stages = [
        ("Upload", len(app_state.uploaded_files) > 0),
        ("Problem Analysis", app_state.problem_analysis_results is not None),
        ("Research", False),
        ("Evidence", False),
        ("Intelligence", False),
        ("Blueprint", False),
    ]

    for name, done in stages:

        if done:
            st.success(name)

        else:
            st.info(name)