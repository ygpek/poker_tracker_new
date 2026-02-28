import pandas as pd


def calculate_cash_summary(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame()

    df = df.assign(
        win=lambda x: x["win"].fillna(0),
    )

    grouped = df.groupby("Player")
    form = {}

    for player, group in grouped:
        last_three = group.sort_values("game_id").tail(3)
        form[player] = last_three["profit_flag"].tolist()

    statistics_advanced = grouped.agg(
        games_played=("game_id", "nunique"),
        total_buy_ins=("buy-in", "sum"),
        average_buy_ins=("buy-in", "mean"),
        kc_won=("win", "sum"),
        kc_won_avg=("win", "mean"),
        won_max=("win", "max"),
        lose_max=("win", "min"),
        variance_won=("win", "std"),
        percent_profit=("profit_flag", "mean"),
    ).reset_index()

    statistics_advanced = statistics_advanced[statistics_advanced["games_played"] >= 3].assign(
        form=lambda x: x["Player"].map(form),
        percent_profit=lambda x: x["percent_profit"] * 100,
    )


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
        "% in profit",
        "Current Form",
    ]

    numeric_cols = [
        "Total buy-ins",
        "Buy-ins per game",
        "Kc won",
        "Kc won per game",
        "Max win",
        "Min win",
        "Win standard deviation",
        "% in profit",
    ]

    for col in numeric_cols:
        statistics_advanced[col] = statistics_advanced[col].round(2)

    return statistics_advanced.sort_values(by="Kc won", ascending=False, ignore_index=True)
