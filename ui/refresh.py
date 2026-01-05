# ui/refresh.py
import streamlit as st


def refresh_data_button():
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("Data refreshed")
