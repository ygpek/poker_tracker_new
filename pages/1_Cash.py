import streamlit as st
from data_load.load_sheet import load_history
from calcs.cash_stats import calculate_cash_summary
from ui.game_selector import game_selector

from ui.refresh import refresh_data_button

VARIABLE = "HISTORY_SHEET_ID"


def highlight_win(val):
    if val > 0:
        color = "green"
    elif val < 0:
        color = "red"
    else:
        color = ""
    return f"color: {color}"


st.set_page_config(page_title="Cash", layout="wide", initial_sidebar_state="expanded")

refresh_data_button()

st.header("💵 Кэш")

df = load_history(VARIABLE)
if df.empty:
    st.warning("No cash games found.")
    st.stop()

# --- Summary table ---
st.subheader("Summary Statistics")
summary_df = calculate_cash_summary(df)

# --- Gradient coloring for kc_won ---
st.dataframe(
    summary_df.style.background_gradient(
        subset=["Kc won"],  # apply gradient only to this column
        cmap="RdYlGn",  # Red → Yellow → Green
    ).format(
        {
            "Total buy-ins": "{:.2f}",
            "Buy-ins per game": "{:.2f}",
            "Kc won per game": "{:.2f}",
            "Win standard deviation": "{:.2f}",
        }
    ),
    hide_index=True,
    width="stretch",
)

# --- Game selector ---
st.subheader("Game history")
game_ids = sorted(df["game_id"].unique())
selected_game = game_selector(game_ids, key="cash_games")

game_df = df[df["game_id"] == selected_game].sort_values(by="win", ascending=False, ignore_index=True)
st.dataframe(
    game_df.style.applymap(
        highlight_win,
        subset=["win"],
    ).format(
        {
            "buy-in": "{:.3f}",
        }
    ),
    hide_index=True,
    width="stretch",
)
