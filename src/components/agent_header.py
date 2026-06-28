import streamlit as st


def show(name: str, description: str, completed: bool):

    st.title(f"🧠 {name}")

    st.write(description)

    if completed:
        st.success("Status: Ready (Previous analysis available)")
    else:
        st.info("Status: Waiting for execution")