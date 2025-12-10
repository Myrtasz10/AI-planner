import streamlit as st
from datetime import date, datetime
from zoneinfo import ZoneInfo
from UI.calendarEventManager import addEvent

def runModals(state) -> None:
    col1, col2, col3 = st.columns(3)

    with col1:
        runAddNewGoalModal(state)
    with col2:
        runAddFreeHoursModal(state)
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
                # ZAMKNIECIE DIALOGU PO KLINIECIU SUBMIT
                st.session_state["show_dialog"] = False
                st.rerun()

    if "setGoal" not in st.session_state:
        if st.button("Dodaj cel"):
            setGoal(dt_pl)
#TODO: delete i update modale dla celi

def runAddFreeHoursModal(state) -> None:
    @st.dialog("Ustaw wolne godziny")
    def setFreeHours(chooseDate):
        with st.form("freeHours"):
            priority_val = st.selectbox("Ustaw dla", [f"Tylko {chooseDate}", "Każdy dzień"])
            startHour = st.time_input("Od")
            endHour = st.time_input("Do")
            #TODO: logika do formatowania datetime (dzien tygodnia, dzien roboczy vs weekend)
            #TODO: kilka przedzialow czasowych na dzien np od 15 do 16 i od 18 do 23
            submitted = st.form_submit_button("Zatwierdź")
            if submitted:
                # WYSŁANIE FORMA DO API
                print(startHour, endHour, priority_val)
                # ZAMKNIECIE DIALOGU PO KLINIECIU SUBMIT
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
#TODO: modal do ustawien uzytkownika

def runUserSettingsModal(state) -> None:
    @st.dialog("Ustawienia")
    def setings():
        with st.form("userSettings"):
            planLength = st.selectbox("Planuj na:", [f"Jutro", "Przyszły tydzień","Przyszły miesiąc"])
            submitted = st.form_submit_button("Zapisz")

    if ("Ustawienia" not in st.session_state):
        if st.button("Zmień ustawienia"):
            setings()