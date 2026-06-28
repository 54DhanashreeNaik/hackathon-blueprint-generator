import pandas as pd
import streamlit as st

from src.utils.file_handlers import format_file_size


def show(app_state):

    if not app_state.uploaded_files:
        return

    data = []

    for f in app_state.uploaded_files:

        data.append(
            {
                "File": f.name,
                "Type": f.content_type,
                "Size": format_file_size(f.size_bytes),
            }
        )

    st.dataframe(
        pd.DataFrame(data),
        width="stretch",
        hide_index=True,
    )