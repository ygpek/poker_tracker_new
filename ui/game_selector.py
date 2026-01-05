import streamlit as st


def game_selector(game_ids, key="game_selector"):
    if not game_ids:
        return None

    # --- session state ---
    if key not in st.session_state:
        # default to last game
        st.session_state[key] = len(game_ids) - 1

    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("⬅️", key=f"{key}_prev"):
            st.session_state[key] = max(0, st.session_state[key] - 1)

    with col3:
        if st.button("➡️", key=f"{key}_next"):
            st.session_state[key] = min(len(game_ids) - 1, st.session_state[key] + 1)

    with col2:
        st.markdown(f"### Game {game_ids[st.session_state[key]]} " f"({st.session_state[key]+1}/{len(game_ids)})")

    return game_ids[st.session_state[key]]
