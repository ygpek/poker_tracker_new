import pandas as pd


def calculate_cash_summary(df: pd.DataFrame) -> pd.DataFrame:
    # TEMP: show player list only
    if df.empty:
        return pd.DataFrame()

    return df[["player"]].drop_duplicates().sort_values("player").reset_index(drop=True)
