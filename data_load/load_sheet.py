import streamlit as st
import pandas as pd
import os
from data_load.gs_client import get_gspread_client


@st.cache_data
def load_history(var: str) -> pd.DataFrame:
    client = get_gspread_client()

    sheet_id = os.environ[var]
    sh = client.open_by_key(sheet_id)
    ws = sh.sheet1

    records = ws.get_all_records()
    df = pd.DataFrame(records)

    return df
