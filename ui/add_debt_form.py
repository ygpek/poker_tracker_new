import streamlit as st
from data_load.append_debt import append_debt


def render_add_debt_form(players):
    st.subheader("➕ Add New Debt")

    with st.form("add_debt_form"):
        from_player = st.selectbox("From (who owes)", players, placeholder="Игорь")
        to_player = st.selectbox("To (who is owed)", players)
        amount = st.number_input("Amount", min_value=1, step=1, value=100)
        note = st.text_input("Note")

        submitted = st.form_submit_button("Add debt")

        if submitted:
            append_debt(
                {
                    "from": from_player,
                    "to": to_player,
                    "amount": amount,
                    "paid": False,
                    "note": note,
                }
            )
            st.success("Debt added")
            st.rerun()
