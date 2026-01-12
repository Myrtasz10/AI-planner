import streamlit as st
from datetime import date, datetime
from zoneinfo import ZoneInfo
from UI.calendarEventManager import addEvent, updateEventsInAPI
from UI.freeDaysSettingsModal import runFreeHoursModal

def runModals(state) -> None:
    col1, col2, col3 = st.columns(3)

    with col1:
        runAddNewGoalModal(state)
    with col2:
        runDeleteGoalModal(state)
    with col2:
        runFreeHoursModal(state)
    with col3:
        runUserSettingsModal(state)
    #TODO: poprawic zeby takich brzydkich przerw nie bylo

def runAddNewGoalModal(state) -> None:
    dt = datetime.now()
    dt_pl = datetime.now()

    if state and "dateClick" in state:
        dt = datetime.fromisoformat(state["dateClick"]["date"])
        dt_pl = dt.astimezone(ZoneInfo("Europe/Warsaw"))
    @st.dialog("Wybierz cel")
    def setGoal(chooseEndDate):
        with st.form("goal"):
            date_val = st.date_input("Deadline:", chooseEndDate.date())
            title_val = st.text_input("Nazwa:", "Nazwij swoj cel")
            desc_val = st.text_input("Opis:", "Opisz swoj cel")
            priority_val = st.selectbox("Priorytet", ["malo wazne", "srednio wazne", "bardzo wazne"])
            submitted = st.form_submit_button("Dodaj")
            if submitted:
                # WYSŁANIE FORMA DO API
                print(date_val, title_val, desc_val, priority_val)
                addEvent(title_val,date_val,date_val,"goal")
                updateEventsInAPI()
                # ZAMKNIECIE DIALOGU PO KLINIECIU SUBMIT
                st.session_state["show_dialog"] = False
                st.rerun()

    if "setGoal" not in st.session_state:
        if st.button("Dodaj cel"):
            setGoal(dt_pl)

def runDeleteGoalModal(state) -> None:
    goals = []
    for event in st.session_state.events:
        if event["groupId"] == "goal":
            goals.append(event)

    @st.dialog("Usuń cel")
    def deleteGoal():
        if not goals:
            st.info("Brak celów do usunięcia")
            return

        goal_map = {
            f"{g['title']} ({g['start'][:10]})": g
            for g in goals
        }

        with st.form("delete_goal_form"):
            selected_label = st.selectbox(
                "Wybierz cel do usunięcia",
                options=list(goal_map.keys()),
            )

            submitted = st.form_submit_button("Usuń")

            if submitted:
                selected_goal = goal_map[selected_label]

                st.session_state.events.remove(selected_goal)
                updateEventsInAPI()
                print("Deleted goal:", selected_goal)
                st.session_state["show_dialog"] = False
                st.success("Cel został usunięty")
                st.rerun()
    if "deleteGoal" not in st.session_state:
        if st.button("Usuń cel"):
            deleteGoal()


def runUserSettingsModal(state) -> None:
    @st.dialog("Ustawienia")
    def setings():
        with st.form("userSettings"):
            planLength = st.selectbox("Planuj na:", [f"Jutro", "Przyszły tydzień","Przyszły miesiąc"])
            submitted = st.form_submit_button("Zapisz")
            if (submitted):
                return
                #TODO: przesłać do modelu wybraną opcję

    if ("Ustawienia" not in st.session_state):
        if st.button("Zmień ustawienia"):
            setings()