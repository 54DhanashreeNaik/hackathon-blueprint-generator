import streamlit as st
from src.agents.blueprint_agent import BlueprintAgent

def show():
    st.title("🗺️ Project Blueprint")
    st.markdown("Assemble architecture diagrams, milestones, tech stacks, and risk plans.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            <div class="premium-card">
                <h3>Blueprint Generation Agent</h3>
                <p>This agent takes all problem contexts, search targets, and technology constraints to formulate a structured roadmap and design specification.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Generate Blueprint", type="primary"):
            with st.spinner("Drafting full project blueprint..."):
                agent = BlueprintAgent()
                result = agent.run({})
                st.session_state.app_state.generated_blueprint = result
                st.success("Blueprint successfully generated!")

    with col2:
        st.markdown("### Agent Status")
        if st.session_state.app_state.generated_blueprint:
            st.markdown('<span class="status-pill success">Idle (Success)</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill warning">Uninitialized</span>', unsafe_allow_html=True)

    bp = st.session_state.app_state.generated_blueprint
    if bp:
        st.markdown("---")
        st.header(f"Project Outline: {bp['project_name']}")
        st.markdown(f"**One Liner:** *{bp['one_liner']}*")
        st.markdown(f"**Target Audience:** {bp['target_audience']}")
        st.markdown(f"**Problem Defined:** {bp['problem_statement']}")
        st.markdown(f"**Proposed Solution:** {bp['proposed_solution']}")

        st.markdown("### 🏗️ Proposed Modules & Architecture")
        for idx, mod in enumerate(bp["architecture"]):
            st.markdown(
                f"""
                <div class="premium-card" style="margin-bottom: 12px;">
                    <h5>{idx+1}. {mod['name']}</h5>
                    <p style="margin: 4px 0;">{mod['description']}</p>
                    <small>Dependencies: {', '.join(mod['dependencies'])}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 🛠️ Tech Stack & Trade-offs")
        for tech in bp["tech_stack"]:
            st.markdown(f"- **{tech['category']}**: `{tech['technology']}` — *{tech['reason']}*")

        st.markdown("### 📆 Implementation Roadmap & Milestones")
        for mile in bp["milestones"]:
            st.markdown(
                f"""
                <div class="premium-card" style="margin-bottom: 10px; border-left: 3px solid #3b82f6;">
                    <strong>{mile['title']} ({mile['duration']})</strong>
                    <ul>
                        {''.join([f"<li>{x}</li>" for x in mile['deliverables']])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### ⚠️ Risk Mitigation Matrix")
        for risk, mitigation in bp["risks_and_mitigations"].items():
            st.markdown(f"- 🔴 **{risk}**:<br/>&nbsp;&nbsp;🛡️ *Mitigation:* {mitigation}", unsafe_allow_html=True)
