import streamlit as st
from src.agents.problem_agent import ProblemUnderstandingAgent


def show():
    st.title("🔍 Problem Analysis")
    st.markdown(
        "Extract guidelines, identify target audiences, technical constraints, assumptions, and risks from your uploaded documents."
    )

    # Check uploads
    if not st.session_state.app_state.uploaded_files:
        st.warning(
            "⚠️ No documents uploaded yet. Please upload files from the Home page first."
        )
        return

    col1, col2 = st.columns([2, 1])

    # ===========================
    # LEFT COLUMN
    # ===========================
    with col1:
        st.markdown(
            """
            <div class="premium-card">
                <h3>🤖 Problem Understanding Agent</h3>
                <p>
                This AI agent reads all uploaded documents, understands the
                hackathon challenge, identifies technical constraints,
                extracts key problems, target users, assumptions, and risks.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🚀 Run Problem Analysis", type="primary"):

            with st.spinner("Analyzing uploaded documents using Gemini..."):

                try:
                    agent = ProblemUnderstandingAgent()

                    result = agent.run(
                        {
                            "uploaded_files":
                                st.session_state.app_state.uploaded_files
                        }
                    )

                    st.session_state.app_state.problem_analysis_results = result

                    st.success("✅ Problem Analysis completed successfully!")

                except Exception as e:
                    st.error("❌ Problem Analysis failed.")
                    st.exception(e)

    # ===========================
    # RIGHT COLUMN
    # ===========================
    with col2:

        st.markdown("### Agent Status")

        if st.session_state.app_state.problem_analysis_results:

            st.success("🟢 Completed")

            result = st.session_state.app_state.problem_analysis_results

            st.metric(
                "Problems",
                len(result.get("extracted_problems", []))
            )

            st.metric(
                "Constraints",
                len(result.get("technical_constraints", []))
            )

            st.metric(
                "Target Users",
                len(result.get("target_audiences", []))
            )

            st.metric(
                "Risks",
                len(result.get("risks", []))
            )

        else:
            st.info("Waiting for execution")

    # ===========================
    # RESULTS
    # ===========================

    result = st.session_state.app_state.problem_analysis_results

    if not result:
        return

    st.divider()

    st.header("📋 Agent Findings")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🎯 Problems",
            "⚙ Constraints",
            "👥 Audience",
            "💡 Assumptions",
            "⚠ Risks",
        ]
    )

    with tab1:

        if result["extracted_problems"]:
            for item in result["extracted_problems"]:
                st.markdown(f"• {item}")
        else:
            st.info("No problems extracted.")

    with tab2:

        if result["technical_constraints"]:
            for item in result["technical_constraints"]:
                st.markdown(f"• {item}")
        else:
            st.info("No constraints identified.")

    with tab3:

        if result["target_audiences"]:
            for item in result["target_audiences"]:
                st.markdown(f"• {item}")
        else:
            st.info("No target audience identified.")

    with tab4:

        if result["assumptions"]:
            for item in result["assumptions"]:
                st.markdown(f"• {item}")
        else:
            st.info("No assumptions extracted.")

    with tab5:

        if result["risks"]:
            for item in result["risks"]:
                st.markdown(f"• {item}")
        else:
            st.info("No risks identified.")

    with st.expander("🔍 Raw Gemini Response"):

        st.json(result)