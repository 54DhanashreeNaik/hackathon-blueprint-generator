import streamlit as st


def show(app_state):

    st.subheader("Uploaded Documents")

    if not app_state.uploaded_files:

        st.warning("No uploaded files.")

        return

    for file in app_state.uploaded_files:

        st.write(f"📄 {file.name}")