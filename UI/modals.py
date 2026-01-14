import streamlit as st
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import sys
import os

# Fix imports to find root modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_manager import add_event_to_db, save_user_setting
from bridge import run_ai_scheduler


def runModals(state) -> None:
    # Changed to 4 columns to include the Action Button seamlessly
    col1, col2, col3 = st.columns([1, 1, 1.5])

    with col1:
        runAddNewGoalModal(state)
    with col2:
        runAddFreeHoursModal(state)
    with col3:
        # THE GENERATE BUTTON
        if st.button("🚀 Generuj Plan", type="primary", use_container_width=True):
            with st.spinner("AI układa Twój dzień..."):
                result = run_ai_scheduler()
                if result["success"]:
                    st.toast(result["message"], icon="✅")
                    st.rerun()
                else:
                    st.error(result["message"])


def runAddNewGoalModal(state) -> None:
    dt = datetime.now()
    if state and "dateClick" in state:
        dt = datetime.fromisoformat(state["dateClick"]["date"])

    @st.dialog("Wybierz cel")
    def setGoal(chooseEndDate):
        with st.form("goal"):
            title_val = st.text_input("Nazwa:", placeholder="Np. Nauka Pythona")
            desc_val = st.text_input("Opis:", placeholder="Szczegóły zadania")
            date_val = st.date_input("Deadline:", chooseEndDate.date())

            # ADDED: Duration is critical for AI
            c1, c2 = st.columns(2)
            with c1:
                duration_val = st.number_input("Czas (min):", min_value=15, value=60, step=15)
            with c2:
                priority_val = st.selectbox("Priorytet", ["mało ważne", "średnio ważne", "bardzo ważne"], index=1)

            submitted = st.form_submit_button("Dodaj Cel", use_container_width=True)

            if submitted:
                # CONNECTED: Saving to DB
                add_event_to_db(
                    title=title_val,
                    start=date_val,
                    end=date_val,
                    group_id="goal",
                    description=desc_val,
                    priority=priority_val,
                    duration=duration_val
                )
                st.session_state["show_dialog"] = False
                st.rerun()

    if "setGoal" not in st.session_state:
        if st.button("➕ Dodaj cel", use_container_width=True):
            setGoal(dt)


def runAddFreeHoursModal(state) -> None:
    @st.dialog("Ustaw wolne godziny")
    def setFreeHours(initialDate):
        with st.form("freeHours"):
            st.write("Kiedy masz czas na zadania?")

            col_start, col_end = st.columns(2)
            with col_start:
                startHour = st.time_input("Od godz:", value=datetime.strptime("09:00", "%H:%M").time())
            with col_end:
                endHour = st.time_input("Do godz:", value=datetime.strptime("17:00", "%H:%M").time())

            picked_date = st.date_input("Dzień", value=initialDate)

            submitted = st.form_submit_button("Zatwierdź", use_container_width=True)

            if submitted:
                # Combine the PICKED date (not necessarily the clicked one) with times
                date_str = picked_date.strftime("%Y-%m-%d")
                start_iso = f"{date_str}T{startHour.strftime('%H:%M:00')}"
                end_iso = f"{date_str}T{endHour.strftime('%H:%M:00')}"

                add_event_to_db(
                    title="Dostępność",
                    start=start_iso,
                    end=end_iso,
                    group_id="availability",
                    description="User defined slot"
                )
                st.session_state["show_dialog"] = False
                st.rerun()

    if ("setFreeHours" not in st.session_state):
        if st.button("🕒 Dostępność", use_container_width=True):
            # Default to today if nothing clicked
            dt_pl = datetime.now()
            if state and "dateClick" in state:
                dt_pl = datetime.fromisoformat(state["dateClick"]["date"])

            setFreeHours(dt_pl)