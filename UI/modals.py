# UI/modals.py
import streamlit as st
import sys
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo
from UI.calendarEventManager import addEvent

# Import the new bridge
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bridge import run_ai_scheduler


def runModals(state) -> None:
    col1, col2, col3 = st.columns(3)

    with col1:
        runAddNewGoalModal(state)
    with col2:
        # Replaced the "Free Hours" button with the Trigger for simplicity
        if st.button("🚀 GENERUJ PLAN", type="primary"):
            with st.spinner("AI analizuje zadania..."):
                result = run_ai_scheduler()
                if result["success"]:
                    st.success("Plan gotowy!")
                    st.rerun()
                else:
                    st.error(f"Błąd: {result['message']}")

    with col3:
        runUserSettingsModal(state)


def runAddNewGoalModal(state) -> None:
    dt = datetime.now()
    if state and "dateClick" in state:
        dt = datetime.fromisoformat(state["dateClick"]["date"])

    @st.dialog("Wybierz cel")
    def setGoal(chooseEndDate):
        with st.form("goal"):
            date_val = st.date_input("Deadline:", chooseEndDate.date())
            title_val = st.text_input("Nazwa:", "Np. Nauka Pythona")
            desc_val = st.text_input("Opis:", "Np. Rozdział 1-3")

            # --- ADDED DURATION FIELD ---
            duration_val = st.number_input("Ile minut to zajmie?", min_value=15, value=60, step=15)

            priority_val = st.selectbox("Priorytet", ["mało ważne (3)", "średnio ważne (2)", "bardzo ważne (1)"])

            submitted = st.form_submit_button("Dodaj")
            if submitted:
                # Pass duration to the updated addEvent function
                # Note: You need to update UI/calendarEventManager.py to accept duration too!
                # Or just call db directly here for simplicity:
                from data_manager import add_event_to_db
                add_event_to_db(title_val, date_val, date_val, "goal", desc_val, priority_val, duration_val)

                st.session_state["show_dialog"] = False
                st.rerun()

    if "setGoal" not in st.session_state:
        if st.button("Dodaj cel"):
            setGoal(dt)

def runUserSettingsModal(state) -> None:
    @st.dialog("Ustawienia")
    def setings():
        with st.form("userSettings"):
            planLength = st.selectbox("Planuj na:", [f"Jutro", "Przyszły tydzień","Przyszły miesiąc"])
            submitted = st.form_submit_button("Zapisz")

    if ("Ustawienia" not in st.session_state):
        if st.button("Zmień ustawienia"):
            setings()