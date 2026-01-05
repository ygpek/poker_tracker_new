import streamlit as st

from ui.refresh import refresh_data_button
from ui.tournament_selector import tournament_selector
from data_load.load_sheet import load_history
from calcs.tournament_stats import calculate_stats_tournaments

VARIABLE = "TOURNAMENT_HISTORY_ID"


def highlight_win(val):
    if val < 4:
        color = "green"
    elif val >= 4:
        color = "red"
    else:
        color = ""
    return f"color: {color}"


st.set_page_config(page_title="Tournaments", layout="wide", initial_sidebar_state="expanded")

refresh_data_button()

st.header("🏆 Турниры")

df = load_history(VARIABLE)
if df.empty:
    st.warning("No cash games found.")
    st.stop()

# --- Summary table ---
st.subheader("Summary Statistics")
summary_df = calculate_stats_tournaments(df)

# --- Gradient coloring for kc_won ---
st.dataframe(
    summary_df.style.background_gradient(
        subset=["Total ITM"],  # apply gradient only to this column
        cmap="RdYlGn",  # Red → Yellow → Green
    ).format(
        {
            "% ITM": "{:.2f}",
        }
    ),
    hide_index=True,
    width="stretch",
)


# --- Game selector ---
st.subheader("Game history")
game_ids = sorted(df["tournament_id"].unique())
selected_game = tournament_selector(game_ids, key="tournament_games")

game_df = df[df["tournament_id"] == selected_game].sort_values(by="place", ascending=True, ignore_index=True)
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
    width="stretch",
)
