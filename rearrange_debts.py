import numpy as np
from data_load.load_debts import load_debts
from data_load.calculate_debts import calculate_debts
from data_load.upload_debts import upload_debts
from data_load.mark_debts_paid import mark_paid_debts


def main():
    debts_df = load_debts()

    active_debts = debts_df[debts_df["paid"] == "FALSE"]
    mark_paid_debts()

    payers_grouped = (
        active_debts.groupby("from")
        .agg(
            amount_to_send=("amount", "sum"),
        )
        .reset_index()
    )
    payees_grouped = (
        active_debts.groupby("to")
        .agg(
            amount_to_receive=("amount", "sum"),
        )
        .reset_index()
    )
    total_debts = payees_grouped.merge(
        payers_grouped,
        left_on="to",
        right_on="from",
        how="outer",
    ).assign(
        player=lambda df: np.where(df["to"].isna(), df["from"], df["to"]),
        amount_to_receive=lambda df: df["amount_to_receive"].fillna(0),
        amount_to_send=lambda df: df["amount_to_send"].fillna(0),
        win=lambda df: df["amount_to_receive"] - df["amount_to_send"],
    )
    calculated_debts = calculate_debts(total_debts)
    upload_debts(calculated_debts, "Перерасчет долгов")


if __name__ == "__main__":
    main()
