from data_load.gs_client import get_gspread_client
from data_load.gc_pandas_utils import load_ws
import os

DEBTS_SHEET_ID = os.environ["DEBTS_SHEET_ID"]
DEBTS_WORKSHEET_NAME = "Debts"


def append_debt(debt):
    """
    debt: dict with keys
    from_player, to_player, amount, reason, created_at, paid, paid_at
    """
    client = get_gspread_client()
    sheet = client.open_by_key(DEBTS_SHEET_ID)
    worksheet = sheet.worksheet(DEBTS_WORKSHEET_NAME)

    debts_df = load_ws(worksheet)

    debt_id = debts_df["debt_id"].max() + 1

    row = [
        str(debt_id),
        debt["from"],
        debt["to"],
        str(debt["amount"]),
        debt["paid"],
        debt["note"],
    ]

    worksheet.append_row(row)


def mark_debt_as_paid(debt_id):
    client = get_gspread_client()
    sheet = client.open_by_key(DEBTS_SHEET_ID)
    worksheet = sheet.worksheet(DEBTS_WORKSHEET_NAME)

    records = worksheet.get_all_records()

    for idx, record in enumerate(records, start=2):  # +2 for header
        if record["debt_id"] == debt_id:
            worksheet.update_cell(idx, 5, True)  # paid
            return
