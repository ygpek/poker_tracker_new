import streamlit as st
from data_load.load_debts import load_debts
from ui.debt_table import render_debt_table
from ui.add_debt_form import render_add_debt_form
from data_load.trigger_workflow import trigger_workflow


st.set_page_config(page_title="Poker Debts", layout="wide", initial_sidebar_state="expanded")

st.title("💰 Poker Debts & Payments")

# --- Load data ---
debts_df = load_debts()

# Filter unpaid debts
active_debts = debts_df[debts_df["paid"] == "FALSE"]

# Collect players dynamically
players = sorted(set(debts_df["from"]).union(set(debts_df["to"])))

# --- Sidebar ---
with st.sidebar:
    st.header("Filters")

    payer_filter = st.selectbox("Show debts for payer:", options=["All"] + players)

    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

# --- Apply filter ---
if payer_filter != "All":
    active_debts = active_debts[active_debts["from"] == payer_filter]

# --- Layout ---
left, right = st.columns([2, 1])

with left:
    render_debt_table(active_debts)

with right:
    render_add_debt_form(players)


# --- Add vertical space before buttons ---
st.markdown("<br><br>", unsafe_allow_html=True)

# --- Workflow button at bottom ---
st.subheader("🔄 Update Cash Games History")
if st.button("Update Cash Games Data"):
    success = trigger_workflow("add_new_debts.yml")
    if success:
        st.success("Cash games update triggered ✅")
    else:
        st.error("Failed to trigger workflow ❌")
