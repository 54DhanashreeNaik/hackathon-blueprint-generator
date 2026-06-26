import streamlit as st
from src.agents.problem_agent import ProblemUnderstandingAgent

def show():
    st.title("🔍 Problem Analysis")
    st.markdown("Extract guidelines, identify target audiences, and define technical constraints.")

    # Show warning if no files uploaded
    if not st.session_state.app_state.uploaded_files:
        st.warning("⚠️ No documents uploaded yet. Go back to Home to upload files for analysis.")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            <div class="premium-card">
                <h3>Problem Understanding Agent</h3>
                <p>This agent parses your files to align constraints, uncover implicit hackathon rules, and document requirements.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Trigger Problem Analysis Agent", type="primary"):
            with st.spinner("Analyzing uploaded materials..."):
                agent = ProblemUnderstandingAgent()
                result = agent.run({"uploaded_files": st.session_state.app_state.uploaded_files})
                st.session_state.app_state.problem_analysis_results = result
                st.success("Analysis complete!")

    with col2:
        st.markdown("### Agent Status")
        if st.session_state.app_state.problem_analysis_results:
            st.markdown('<span class="status-pill success">Idle (Success)</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill warning">Uninitialized</span>', unsafe_allow_html=True)

    # Render results
    res = st.session_state.app_state.problem_analysis_results
    if res:
        st.markdown("---")
        st.markdown("### 📋 Agent Findings")
        
        tab1, tab2, tab3 = st.tabs(["Key Problems", "Constraints", "Target Audience"])
        
        with tab1:
            for item in res["extracted_problems"]:
                st.markdown(f"- {item}")
        with tab2:
            for item in res["technical_constraints"]:
                st.markdown(f"- {item}")
        with tab3:
            for item in res["target_audiences"]:
                st.markdown(f"- {item}")
                
        with st.expander("Show Agent System Prompts & Trace Log"):
            st.code(res["raw_output"])
