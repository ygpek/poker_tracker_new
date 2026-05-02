import streamlit as st
from datetime import date, time
import pandas as pd
from data_load.events import load_events, save_events

st.title("📅 Poker Calendar")

with st.sidebar:
    st.header("Filters")

    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

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
        st.cache_data.clear()
        st.rerun()

df = load_events()

active_events = df[df["date"] >= date.today()]
st.header("Upcoming Games")
if active_events.empty:
    st.info("No upcoming games scheduled.")
else:
    for _, row in active_events.iterrows():
        with st.container(border=True):

            st.write(f"📅 Date: {row['date']}")
            st.write(f"🕒 Time: {row['time']}")
            st.write(f"🎲 Type: {row['type']}")

            players = row["players"].split(",") if row["players"] else []

            st.write("👥 Players: " + (", ".join(players) if players else "Nobody yet"))

            event_id = row["event_id"]

            if st.button("Add Player", key=f"show_add_{event_id}"):
                st.session_state[f"adding_player_{event_id}"] = True

            if st.session_state.get(f"adding_player_{event_id}", False):

                new_player = st.text_input("Player name", key=f"new_player_{event_id}")

                if st.button("Confirm Add", key=f"confirm_add_{event_id}"):
                    new_player = new_player.strip()

                    if new_player:
                        if new_player not in players:
                            players.append(new_player)

                            df.loc[df["event_id"] == event_id, "players"] = ",".join(players)

                            save_events(df)

                            st.session_state[f"adding_player_{event_id}"] = False

                            st.success(f"{new_player} added ✅")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.warning("Player already registered.")

                # -------------------
                # Remove player section
                # -------------------
            if players:
                player_to_remove = st.selectbox("Remove player", players, key=f"remove_select_{event_id}")

                if st.button("Remove", key=f"remove_btn_{event_id}"):
                    players.remove(player_to_remove)

                    df.loc[df["event_id"] == event_id, "players"] = ",".join(players)

                    save_events(df)
                    st.success(f"{player_to_remove} removed")
                    st.cache_data.clear()
                    st.rerun()
