import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from data_load.gc_pandas_utils import load_ws

POKER_SHEET_ID = os.environ["POKER_SHEET_ID"]

POKER_COLS = ["Player", "buy-in", "win"]


def return_new_game() -> pd.DataFrame:
    creds_json = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    gc = gspread.authorize(creds)

    source_sheet = gc.open_by_key(POKER_SHEET_ID)
    source_ws = source_sheet.worksheet("game")
    source_df = load_ws(source_ws)[POKER_COLS]
    return source_df
