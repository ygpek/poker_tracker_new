import streamlit as st

# --- Ensure sidebar is visible ---
st.set_page_config(page_title="Poker Statistics", layout="wide", initial_sidebar_state="expanded")  # <- key line

st.title("♠️ Poker Statistics")

# Sidebar content
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Refresh data"):
        st.cache_data.clear()
        st.success("Data refreshed")
