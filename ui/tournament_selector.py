import streamlit as st


def tournament_selector(game_ids, key="tournament_selector"):
    if not game_ids:
        return None

    if key not in st.session_state:
        st.session_state[key] = len(game_ids) - 1  # start at latest game

    current_index = st.session_state[key]

    col1, col2, col3 = st.columns([1, 2, 1])

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
        st.markdown(
            f"### Tournament #{game_ids[st.session_state[key]]} " f"({st.session_state[key]+1}/{len(game_ids)})"
        )

    # --- Jump-to selectbox ---
    selected_game = st.selectbox(
        "Jump to game:",
        options=sorted(game_ids, reverse=True),
        index=current_index,
        key=f"{key}_jump",
        format_func=lambda x: f"Game {x}",
    )

    # Update session state if selectbox changed
    if selected_game != game_ids[st.session_state[key]]:
        st.session_state[key] = game_ids.index(selected_game)

    return game_ids[st.session_state[key]]
