import streamlit as st
from datetime import date
import pandas as pd
from data_load.events import load_events, save_events

st.title("📅 Poker Calendar")

with st.expander("Create new event"):
    event_date = st.date_input("Date", min_value=date.today())
    game_type = st.selectbox("Game Type", ["Cash", "Tournament"])

    if st.button("Create Event"):
        df = load_events()

        new_row = {
            "event_id": len(df) + 1,
            "date": event_date,
            "type": type,
            "participants": "",
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_events(df)

        st.success("Event created ✅")
        st.rerun()

df = load_events()
df["date"] = pd.to_datetime(df["date"], format="%m/%d/s%y")

active_events = df[df["date"] >= date.today().strftime("%m/%d/%Y")]
