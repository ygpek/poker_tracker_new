import os

from data_load.upload_debts import upload_debts
from data_load.calculate_debts import calculate_debts
from data_load.add_new_game import return_new_game


DEBTS_SHEET_ID = os.environ["DEBTS_SHEET_ID"]
DEBTS_COLS = ["debt_id", "from", "to", "amount", "paid", "note"]


def main():

    new_game = return_new_game()
    debts_new = calculate_debts(new_game)

    upload_debts(debts_new)


if __name__ == "__main__":
    main()
