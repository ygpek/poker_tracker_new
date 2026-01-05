import streamlit as st
from data_load.cash_games import load_cash_games
from calcs.cash_stats import calculate_cash_summary
from ui.game_selector import game_selector

st.header("💵 Cash Games")

df = load_cash_games()
if df.empty:
    st.warning("No cash games found.")
    st.stop()

# --- Summary table ---
st.subheader("Summary Statistics")
summary_df = calculate_cash_summary(df)

# --- Gradient coloring for kc_won ---
st.dataframe(
    summary_df.style.background_gradient(
        subset=["kc_won"],  # apply gradient only to this column
        cmap="RdYlGn",  # Red → Yellow → Green
    ),
    use_container_width=True,
)

# --- Game selector ---
st.subheader("Game history")
game_ids = sorted(df["game_id"].unique())
selected_game = game_selector(game_ids, key="cash_games")

game_df = df[df["game_id"] == selected_game]
st.dataframe(game_df, use_container_width=True)
