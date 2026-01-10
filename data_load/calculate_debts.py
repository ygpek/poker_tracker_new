import pandas as pd
from add_new_game import return_new_game


def calculate_debts() -> pd.DataFrame:
    new_game = return_new_game()
    payers = new_game[new_game["win"] < 0].sort_values(by="win").reset_index(drop=True)
    payees = new_game[new_game["win"] > 0].sort_values(by="win", ascending=False).reset_index(drop=True)
    i, j = (
        0,
        0,
    )
    transactions = pd.DataFrame(columns=["payer", "payee", "amount"])
    while i < len(payees) and j < len(payers):
        payer = payers.loc[j, "Player"]
        payee = payees.loc[i, "Player"]
        amount = min(payees.loc[i, "win"], abs(payers.loc[j, "win"]))
        transactions.loc[len(transactions)] = [payer, payee, amount]
        payees.loc[i, "win"] -= amount
        payers.loc[j, "win"] += amount
        if payees.loc[i, "win"] == 0:
            i += 1
        if payers.loc[j, "win"] == 0:
            j += 1
    return transactions
