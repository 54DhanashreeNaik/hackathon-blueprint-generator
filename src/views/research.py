import streamlit as st
from src.agents.research_agent import ResearchAgent

def show():
    st.title("🌐 Research")
    st.markdown("Query API directories, GitHub repos, and competitor solutions.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            <div class="premium-card">
                <h3>Research Agent</h3>
                <p>This agent will query Tavily, Google, and repository APIs to discover technologies and reference code relevant to the problem.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Trigger Research Agent", type="primary"):
            with st.spinner("Executing queries and scanning libraries..."):
                agent = ResearchAgent()
                result = agent.run({})
                st.session_state.app_state.research_results = result
                st.success("Research completed!")

    with col2:
        st.markdown("### Agent Status")
        if st.session_state.app_state.research_results:
            st.markdown('<span class="status-pill success">Idle (Success)</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill warning">Uninitialized</span>', unsafe_allow_html=True)

    res = st.session_state.app_state.research_results
    if res:
        st.markdown("---")
        st.markdown("### 🔍 Research Discoveries")

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("#### Automated Search Targets")
            for q in res["search_queries"]:
                st.markdown(f"- `{q}`")
        with col_right:
            st.markdown("#### Recommended Integrations & APIs")
            for api in res["recommended_apis"]:
                st.markdown(f"**{api['name']}**: {api['use_case']}")

        with st.expander("Show Agent Log"):
            st.code(res["raw_output"])
