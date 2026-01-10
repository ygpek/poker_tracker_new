import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from gc_pandas_utils import load_ws
from calculate_debts import calculate_debts


DEBTS_SHEET_ID = os.environ["DEBTS_SHEET_ID"]
DEBTS_COLS = ["debt_id", "from", "to", "amount", "paid", "note"]


def main():

    creds_json = json.loads(os.environ["GCP_SERVICE_ACCOUNT"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_json, scopes=scopes)
    gc = gspread.authorize(creds)

    debts_new = calculate_debts()

    debts_sheet = gc.open_by_key(DEBTS_SHEET_ID)
    debts_ws = debts_sheet.worksheet("Debts")
    debts_df = load_ws(debts_ws)[DEBTS_COLS]

    debt_id = debts_df["debt_id"].max() + 1

    for row in debts_new.values.tolist():
        row_to_append = [debt_id.astype(str), row[0], row[1], row[2], False, ""]
        debt_id = debt_id + 1
        debts_ws.append_row(row_to_append, value_input_option="USER_ENTERED")


if __name__ == "__main__":
    main()
