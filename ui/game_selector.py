import streamlit as st


def game_selector(game_ids):
    if not game_ids:
        return None

    if "game_idx" not in st.session_state:
        st.session_state.game_idx = 0

    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("⬅️"):
            st.session_state.game_idx = max(0, st.session_state.game_idx - 1)

    with col3:
        if st.button("➡️"):
            st.session_state.game_idx = min(len(game_ids) - 1, st.session_state.game_idx + 1)

    with col2:
        st.markdown(f"### Game {game_ids[st.session_state.game_idx]}")

    return game_ids[st.session_state.game_idx]
