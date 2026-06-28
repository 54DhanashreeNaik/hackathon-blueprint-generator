import streamlit as st

from src.models.state import UploadedFileMetadata
from src.utils.file_handlers import save_uploaded_file

from src.components import (
    hero,
    dashboard,
    workflow,
    upload_table,
    footer,
)


def show():

    app_state = st.session_state.app_state

    # ---------------------------------------------------------
    # Hero
    # ---------------------------------------------------------
    hero.show()

    # ---------------------------------------------------------
    # Dashboard
    # ---------------------------------------------------------
    dashboard.show(app_state)

    st.divider()

    # ---------------------------------------------------------
    # Upload Section
    # ---------------------------------------------------------
    st.header("📥 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload Hackathon briefs, datasets, research papers or documentation",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="file_uploader_widget",
    )

    if uploaded_files:

        for file in uploaded_files:

            already_uploaded = any(
                existing.name == file.name
                for existing in app_state.uploaded_files
            )

            if already_uploaded:
                continue

            file_bytes = file.read()

            saved_path = save_uploaded_file(
                file_bytes=file_bytes,
                filename=file.name,
            )

            if saved_path:

                meta = UploadedFileMetadata(
                    name=file.name,
                    size_bytes=len(file_bytes),
                    content_type=file.type,
                    local_path=str(saved_path),
                )

                app_state.uploaded_files.append(meta)

                st.toast(
                    f"{file.name} uploaded successfully!",
                    icon="✅",
                )

    st.divider()

    # ---------------------------------------------------------
    # Workflow
    # ---------------------------------------------------------
    workflow.show(app_state)

    st.divider()

    # ---------------------------------------------------------
    # Uploaded Files
    # ---------------------------------------------------------
    st.subheader("📄 Uploaded Files")

    upload_table.show(app_state)

    # ---------------------------------------------------------
    # Navigation Message
    # ---------------------------------------------------------
    if len(app_state.uploaded_files) == 0:

        st.info(
            "Upload one or more documents to begin."
        )

    elif app_state.problem_analysis_results is None:

        st.success(
            "Documents uploaded successfully.\n\n➡ Continue to **Problem Analysis** using the left sidebar."
        )

    else:

        st.success(
            "Problem Analysis completed.\n\n➡ Continue to **Research**."
        )

    # ---------------------------------------------------------
    # Clear Button
    # ---------------------------------------------------------
    if app_state.uploaded_files:

        if st.button(
            "🗑 Clear Uploaded Files",
            type="secondary",
        ):

            app_state.uploaded_files.clear()
            app_state.problem_analysis_results = None

            st.rerun()

    footer.show()