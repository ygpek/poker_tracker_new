import os
import json
import gspread
from google.oauth2.service_account import Credentials
from gc_pandas_utils import load_ws

DEBTS_SHEET_ID = os.environ["DEBTS_SHEET_ID"]
DEBTS_COLS = ["debt_id", "from", "to", "amount", "paid", "note"]


def mark_paid_debts() -> None:
    creds_json = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    gc = gspread.authorize(creds)
    debts_sheet = gc.open_by_key(DEBTS_SHEET_ID)
    debts_ws = debts_sheet.worksheet("Debts")
    debts_df = load_ws(debts_ws)[DEBTS_COLS]
    debts_df["paid"] = True
    debts_ws.update([debts_df.columns.values.tolist()] + debts_df.values.tolist())
