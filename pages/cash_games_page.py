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
st.subheader("Summary (placeholder)")
summary_df = calculate_cash_summary(df)
st.dataframe(summary_df, use_container_width=True)

# --- Game history ---
st.subheader("Game history")

game_ids = sorted(df["game_id"].unique())
selected_game = game_selector(game_ids)

game_df = df[df["game_id"] == selected_game]
st.dataframe(game_df, use_container_width=True)
