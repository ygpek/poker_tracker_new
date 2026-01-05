import streamlit as st


def game_selector(game_ids, key="game_selector"):
    if not game_ids:
        return None

    if key not in st.session_state:
        st.session_state[key] = len(game_ids) - 1  # start at latest game

    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        st.session_state[key] = max(0, st.session_state[key])  # safety
        st.button(
            "⬅️",
            key=f"{key}_prev",
            disabled=st.session_state[key] == 0,
            on_click=lambda: st.session_state.__setitem__(key, st.session_state[key] - 1),
        )

    with col3:
        st.session_state[key] = min(len(game_ids) - 1, st.session_state[key])  # safety
        st.button(
            "➡️",
            key=f"{key}_next",
            disabled=st.session_state[key] == len(game_ids) - 1,
            on_click=lambda: st.session_state.__setitem__(key, st.session_state[key] + 1),
        )

    with col2:
        st.markdown(f"### Game # {game_ids[st.session_state[key]]} " f"({st.session_state[key]+1}/{len(game_ids)})")

    return game_ids[st.session_state[key]]
