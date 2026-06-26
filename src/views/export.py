import streamlit as st
from src.services.pdf_service import PDFService
from config.settings import REPORT_DIR

def show():
    st.title("📤 Export Blueprint")
    st.markdown("Download generated specs, reports, and architecture plans.")

    bp = st.session_state.app_state.generated_blueprint
    
    if not bp:
        st.warning("⚠️ No blueprint generated yet. Run the generator in the Blueprint tab first.")
        return

    st.markdown(
        """
        <div class="premium-card">
            <h3>Download Center</h3>
            <p>Your hackathon blueprint is ready for export. Export as Markdown for your project readme, or generate a PDF file for pitches.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        # Markdown export
        md_content = f"""# Project Blueprint: {bp.get('project_name')}
One Liner: {bp.get('one_liner')}

## Problem Statement
{bp.get('problem_statement')}

## Solution
{bp.get('proposed_solution')}
"""
        st.download_button(
            label="💾 Download Markdown (.md)",
            data=md_content,
            file_name="blueprint.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        # PDF export using service
        pdf_service = PDFService()
        pdf_path = pdf_service.generate_pdf_blueprint(bp, f"{bp['project_name'].lower().replace(' ', '_')}_blueprint.pdf")
        
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="📄 Download PDF (.pdf)",
            data=pdf_bytes,
            file_name=pdf_path.name,
            mime="application/pdf",
            use_container_width=True
        )

    st.success("Exports compiled successfully! Click above to download.")
