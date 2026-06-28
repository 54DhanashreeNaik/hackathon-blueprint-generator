import streamlit as st


def show(result):

    if result is None:
        return

    with st.expander("📌 Extracted Problems", expanded=True):

        for item in result["extracted_problems"]:

            st.write("•", item)

    with st.expander("⚙ Technical Constraints"):

        for item in result["technical_constraints"]:

            st.write("•", item)

    with st.expander("👥 Target Audience"):

        for item in result["target_audiences"]:

            st.write("•", item)

    with st.expander("💡 Assumptions"):

        for item in result.get("assumptions", []):

            st.write("•", item)

    with st.expander("⚠ Risks"):

        for item in result.get("risks", []):

            st.write("•", item)

    with st.expander("Raw LLM Output"):

        st.code(result["raw_output"])