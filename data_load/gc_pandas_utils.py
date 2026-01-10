import pandas as pd

def load_ws(ws):
    records = ws.get_all_records()
    return pd.DataFrame(records) if records else pd.DataFrame()