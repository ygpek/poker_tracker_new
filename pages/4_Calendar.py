import streamlit as st
from datetime import date, time
import pandas as pd
from data_load.events import load_events, save_events

st.title("📅 Poker Calendar")

with st.expander("Create new event"):
    game_type = st.selectbox("Game Type", ["Cash", "Tournament"])
    event_date = st.date_input("Date", min_value=date.today())

    event_time = st.time_input("Time", value=time(19, 0))

    if st.button("Create Event"):
        df = load_events()

        new_row = {
            "event_id": len(df) + 1,
            "date": event_date.strftime("%Y-%m-%d"),
            "time": event_time.strftime("%H:%M"),
            "type": game_type,
            "players": "",
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_events(df)

        st.success("Event created ✅")
        st.rerun()

df = load_events()
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

active_events = df[df["date"] >= date.today().strftime("%m/%d/%Y")]
st.header("Upcoming Games")
if active_events.empty:
    st.info("No upcoming games scheduled.")
else:
    for _, row in active_events.iterrows():
        with st.container(border=True):

            st.write(f"📅 Date: {row['date']}")
            st.write(f"🎲 Type: {row['type']}")

            players = row["players"].split(",") if row["players"] else []

            st.write("👥 Players: " + (", ".join(players) if players else "Nobody yet"))
