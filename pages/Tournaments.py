import streamlit as st

from ui.refresh import refresh_data_button
from ui.tournament_selector import tournament_selector
from data_load.load_sheet import load_history

VARIABLE = "TOURNAMENT_HISTORY_ID"


def highlight_win(val):
    if val < 4:
        color = "green"
    elif val >= 4:
        color = "red"
    else:
        color = ""
    return f"color: {color}"


refresh_data_button()

df = load_history(VARIABLE)


# --- Game selector ---
st.subheader("Game history")
game_ids = sorted(df["tournament_id"].unique())
selected_game = tournament_selector(game_ids, key="tournament_games")

game_df = df[df["game_id"] == selected_game].sort_values(by="place", ascending=True, ignore_index=True)
st.dataframe(
    game_df.style.applymap(
        highlight_win,
        subset=["place"],
    ).format(
        {
            "place": "{:.0f}",
        }
    ),
    hide_index=True,
    use_container_width=True,
)
