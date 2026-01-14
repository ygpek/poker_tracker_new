import streamlit as st
from data_load.append_debt import mark_debt_as_paid


def render_debt_table(debts_df):
    st.subheader("💸 Outstanding Debts")

    if debts_df.empty:
        st.success("No outstanding debts 🎉")
        return

    for _, row in debts_df.iterrows():
        col1, col2, col3, col4 = st.columns([3, 3, 2, 1])

        with col1:
            st.write(f"**{row['from']} → {row['to']}**")

        with col2:
            st.write(row["note"])

        with col3:
            st.write(f"{row['amount']:.2f}")

        with col4:
            if st.button("✅ Paid", key=f"paid_{row['debt_id']}"):
                mark_debt_as_paid(row["debt_id"])
                st.cache_data.clear()
                st.rerun()
