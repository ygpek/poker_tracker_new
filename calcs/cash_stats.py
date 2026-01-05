import pandas as pd


def calculate_cash_summary(df: pd.DataFrame) -> pd.DataFrame:
    # TEMP: show player list only
    if df.empty:
        return pd.DataFrame()

    df = df.assign(
        win=lambda x: x["win"].fillna(0),
    )

    grouped = df.groupby("Player")

    statistics_advanced = grouped.agg(
        games_played=("game_id", "nunique"),
        total_buy_ins=("buy-in", "sum"),
        average_buy_ins=("buy-in", "mean"),
        kc_won=("win", "sum"),
        kc_won_avg=("win", "mean"),
        won_max=("win", "max"),
        lose_max=("win", "min"),
        variance_won=("win", "std"),
    ).reset_index()

    return statistics_advanced.sort(by="kc_won", ascending=False)
