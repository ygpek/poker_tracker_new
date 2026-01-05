import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from gc_pandas_utils import load_ws


POKER_SHEET_ID = os.environ["NEW_TOURNAMENT_ID"]
HISTORY_SHEET_ID = os.environ["TOURNAMENT_HISTORY_ID"]
POKER_COLS = ["player", "place"]
HISTORY_COLS = ["tournament_id", "player", "place"]


def main():

    creds_json = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    gc = gspread.authorize(creds)

    source_sheet = gc.open_by_key(POKER_SHEET_ID)
    source_ws = source_sheet.worksheet("History")
    source_df = load_ws(source_ws)[POKER_COLS]

    history_sheet = gc.open_by_key(HISTORY_SHEET_ID)
    history_ws = history_sheet.worksheet("Tournament")
    history_df = load_ws(history_ws)[HISTORY_COLS]

    new_game_id = history_df["game_id"].max() + 1
    source_df = source_df.assign(
        game_id=new_game_id,
    )[HISTORY_COLS]

    for row in source_df.values.tolist():
        history_ws.append_row(row, value_input_option="USER_ENTERED")


if __name__ == "__main__":
    main()
