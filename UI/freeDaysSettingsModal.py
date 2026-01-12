import streamlit as st
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

def runFreeHoursModal(state) -> None:
    if "free_hours_intervals" not in st.session_state:
        st.session_state["free_hours_intervals"] = [
            {"start": time(9, 0), "end": time(17, 0)}
        ]
    @st.dialog("Ustaw wolne godziny")
    def setFreeHours(chooseDate):
        with st.form("freeHours"):
            priority_val = st.selectbox(
                "Ustaw dla",
                [
                    f"Tylko {chooseDate.date()}",
                    f"Każdy {formatDate(chooseDate)}",
                    f"Każdy {formatThirdOption(chooseDate)}",
                    "Każdy dzień",
                ],
            )
            st.markdown("### Przedziały czasowe")

            intervals = st.session_state["free_hours_intervals"]

            for i, interval in enumerate(intervals):
                col1, col2, col3 = st.columns([3, 3, 1])

                with col1:
                    interval["start"] = st.time_input(
                        "Od",
                        value=interval["start"],
                        key=f"start_{i}",
                    )

                with col2:
                    interval["end"] = st.time_input(
                        "Do",
                        value=interval["end"],
                        key=f"end_{i}",
                    )

                with col3:
                    if st.form_submit_button("❌", key=f"remove_{i}"):
                        intervals.pop(i)
                        st.rerun()
            if st.button("➕ Dodaj przedział"):
                st.session_state["free_hours_intervals"].append(
                    {"start": time(9, 0), "end": time(17, 0)}
                )
                st.rerun()
            submitted = st.form_submit_button("Zatwierdź")
            if submitted:
                intervals = st.session_state["free_hours_intervals"]

                payload = {
                    "priority": priority_val,
                    "intervals": [
                        {"from": i["start"].isoformat(), "to": i["end"].isoformat()}
                        for i in intervals
                    ],
                }

                print(payload)#TODO: send to API

                del st.session_state["free_hours_intervals"]
                st.session_state["show_dialog"] = False
                st.rerun()

    if("setFreeHours" not in st.session_state):
        if st.button("Dodaj godziny"):
            dt = datetime.now()
            dt_pl = datetime.now()

            if state and "dateClick" in state:
                dt = datetime.fromisoformat(state["dateClick"]["date"])
                dt_pl = dt.astimezone(ZoneInfo("Europe/Warsaw"))
            setFreeHours(dt_pl)

def formatDate(chooseDate) -> datetime:
    return chooseDate.strftime("%A")

def formatThirdOption(chooseDate)->str:
    if chooseDate.weekday() < 5:
        return "dzień roboczy"
    else:
        return "weekend"
