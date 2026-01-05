from ui.refresh import refresh_data_button
from data_load.load_sheet import load_history

VARIABLE = "TOURNAMENT_HISTORY_ID"


refresh_data_button()

df = load_history(VARIABLE)
