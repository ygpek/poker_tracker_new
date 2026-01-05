import pandas as pd


def calculate_cash_summary(df: pd.DataFrame) -> pd.DataFrame:

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

    statistics_advanced = statistics_advanced[statistics_advanced["games_played"] >= 3]

    statistics_advanced.columns = [
        "Player",
        "Total Games",
        "Total buy-ins",
        "Buy-ins per game",
        "Kc won",
        "Kc won per game",
        "Max win",
        "Min win",
        "Win standard deviation",
    ]

    numeric_cols = [
        "Total buy-ins",
        "Buy-ins per game",
        "Kc won",
        "Kc won per game",
        "Max win",
        "Min win",
        "Win standard deviation",
    ]

    for col in numeric_cols:
        statistics_advanced[col] = statistics_advanced[col].round(2)

    return statistics_advanced.sort_values(by="Kc won", ascending=False, ignore_index=True)
