import pandas as pd
import numpy as np


def calculate_stats_tournaments(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame()

    df = df.assign(
        first=lambda x: np.where(x["place"] == 1, 1, 0),
        second=lambda x: np.where(x["place"] == 2, 1, 0),
        third=lambda x: np.where(x["place"] == 3, 1, 0),
        itm=lambda x: np.where(x["place"] < 4, 1, 0),
    )

    grouped = df.groupby("player")

    statistics_advanced = grouped.agg(
        total_first=("first", "sum"),
        total_second=("second", "sum"),
        total_third=("third", "sum"),
        total_played=("tournament_id", "nunique"),
        total_itm=("itm", "sum"),
    ).reset_index()

    statistics_advanced = statistics_advanced[statistics_advanced["total_itm"] >= 1]

    statistics_advanced["itm_percentage"] = (
        statistics_advanced["total_itm"] / statistics_advanced["total_played"]
    ) * 100

    statistics_advanced = statistics_advanced[
        [
            "player",
            "total_first",
            "total_second",
            "total_third",
            "total_itm",
            "total_played",
            "itm_percentage",
        ]
    ]

    statistics_advanced.columns = [
        "Player",
        "First",
        "Second",
        "Third",
        "Total ITM",
        "Total played",
        "% ITM",
    ]

    numeric_cols = ["% ITM"]

    for col in numeric_cols:
        statistics_advanced[col] = statistics_advanced[col].round(2)

    return statistics_advanced.sort_values(by=["First", "Second", "Total ITM"], ascending=False, ignore_index=True)
