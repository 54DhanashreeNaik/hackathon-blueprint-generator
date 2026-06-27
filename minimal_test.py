import streamlit as st

def page1():
    st.title("Page 1")

def page2():
    st.title("Page 2")

pg = st.navigation([
    st.Page(page1, title="Page 1", url_path="page1"),
    st.Page(page2, title="Page 2", url_path="page2"),
])

pg.run()