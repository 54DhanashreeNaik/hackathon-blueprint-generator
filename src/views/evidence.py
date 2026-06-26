import streamlit as st
from src.agents.synthesis_agent import SynthesisAgent

def show():
    st.title("📊 Evidence")
    st.markdown("Assess collected datasets, papers, existing libraries, and confidence scores.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            <div class="premium-card">
                <h3>Evidence Synthesis Agent</h3>
                <p>This agent validates collected APIs, papers, and libraries to ensure standard formatting, security compliance, and assigns compatibility confidence scores.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Synthesize Evidence", type="primary"):
            with st.spinner("Synthesizing evidence and scores..."):
                agent = SynthesisAgent()
                result = agent.run({})
                st.session_state.app_state.evidence_items = result.get("evidence_sources", [])
                st.session_state.app_state.intelligence_insights = result # Save full payload
                st.success("Evidence processed!")

    with col2:
        st.markdown("### Agent Status")
        if st.session_state.app_state.evidence_items:
            st.markdown('<span class="status-pill success">Idle (Success)</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill warning">Uninitialized</span>', unsafe_allow_html=True)

    items = st.session_state.app_state.evidence_items
    if items:
        st.markdown("---")
        st.markdown("### 🧬 Validated Evidence & Confidence Scores")

        for item in items:
            score = item["confidence_score"] * 100
            score_color = "#34d399" if score >= 90 else "#fbbf24"
            st.markdown(
                f"""
                <div class="premium-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4>{item['title']}</h4>
                        <span class="status-pill" style="border-color: {score_color}; color: {score_color};">
                            Confidence: {score:.0f}%
                        </span>
                    </div>
                    <p style="margin-top: 8px;"><strong>Category:</strong> {item['category']}</p>
                    <p><strong>Relevance:</strong> {item['relevance']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
