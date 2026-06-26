import streamlit as st
from src.utils.file_handlers import save_uploaded_file, format_file_size, is_supported_file
from src.models.state import UploadedFileMetadata

def show():
    st.title("🚀 Hackathon Blueprint Generator")
    
    # Hero Introduction
    st.markdown(
        """
        <div class="premium-card">
            <h3>Accelerate your Hackathon Ideation with AI Agents</h3>
            <p>Welcome to the Hackathon Blueprint Generator! This application scaffolds your planning process from a rough problem statement or dataset into a production-ready technical blueprint. Designed using an agentic, modular workflow, it ensures your project starts with sound architecture, robust research, and validated scope limits.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Workflow Steps
    st.subheader("💡 End-to-End Workflow")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="premium-card workflow-step">
                <h4>1. Scope & Analysis</h4>
                <p>Upload challenge documents to dissect guidelines, technical constraints, and define target audiences.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="premium-card workflow-step">
                <h4>2. Web Research</h4>
                <p>Run automated web search agent queries to gather competitive products, APIs, and evidence datasets.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="premium-card workflow-step">
                <h4>3. Synthesize & Build</h4>
                <p>Synthesize evidence, validate tech stacks, and compile a comprehensive milestone report.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Ingestion Card
    st.subheader("📥 Ingestion Portal")
    st.markdown("Supported Formats: **PDF, DOCX, TXT, PNG, JPG**")

    uploaded_files = st.file_uploader(
        "Upload Hackathon briefs, reference manuals, datasets, or design mockups",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="file_uploader_widget"
    )

    if uploaded_files:
        for file in uploaded_files:
            # Check if file is already processed
            already_uploaded = any(x.name == file.name for x in st.session_state.app_state.uploaded_files)
            if not already_uploaded:
                file_bytes = file.read()
                saved_path = save_uploaded_file(file_bytes, file.name)
                if saved_path:
                    meta = UploadedFileMetadata(
                        name=file.name,
                        size_bytes=len(file_bytes),
                        content_type=file.type,
                        local_path=str(saved_path)
                    )
                    st.session_state.app_state.uploaded_files.append(meta)
                    st.toast(f"Saved {file.name} successfully!", icon="✅")

    # Display upload info
    if st.session_state.app_state.uploaded_files:
        st.markdown("### 📋 Uploaded Files Metadata")
        for idx, file_meta in enumerate(st.session_state.app_state.uploaded_files):
            size_formatted = format_file_size(file_meta.size_bytes)
            st.markdown(
                f"""
                <div class="premium-card" style="padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>📄 {file_meta.name}</strong><br/>
                        <span style="font-size: 0.85em; color: rgba(255,255,255,0.6);">
                            Type: {file_meta.content_type} | Size: {size_formatted}
                        </span>
                    </div>
                    <span class="status-pill success">Stored</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        if st.button("Clear Uploaded Files"):
            st.session_state.app_state.uploaded_files = []
            st.rerun()
    else:
        st.info("No documents uploaded yet. Upload templates to get started.")

    # Footer
    st.markdown(
        """
        <div class="footer-text">
            Hackathon Blueprint Generator • Design System v1.0.0 • Built with Streamlit and Antigravity
        </div>
        """,
        unsafe_allow_html=True
    )
