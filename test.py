import streamlit as st

st.title("Test Page")

st.markdown(
    "<h1 style='color:red'>THIS SHOULD BE RED</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        background:#222;
        color:white;
        padding:20px;
        border-radius:15px;
        border:1px solid #555;
    ">
        <h2>Premium Card</h2>
        <p>If you can read this inside a dark box, HTML is working.</p>
    </div>
    """,
    unsafe_allow_html=True,
)