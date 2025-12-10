import streamlit as st
from datetime import date, datetime
from streamlit_calendar import calendar
from zoneinfo import ZoneInfo

def runModals(state) -> None:
    runAddNewGoalModal(state)

def runAddNewGoalModal(state) -> None:
    dt = datetime.now()
    dt_pl = datetime.now()

    if state and "dateClick" in state:
        dt = datetime.fromisoformat(state["dateClick"]["date"])
        dt_pl = dt.astimezone(ZoneInfo("Europe/Warsaw"))
    @st.dialog("Wybierz cel")
    def choose(chooseEndDate):
        with st.form("goal"):
            date_val = st.date_input("Deadline:", chooseEndDate.date())
            title_val = st.text_input("Nazwa:", "Nazwij swoj cel")
            desc_val = st.text_input("Opis:", "Opisz swoj cel")
            priority_val = st.selectbox("Priorytet", ["malo wazne", "srednio wazne", "bardzo wazne"])
            submitted = st.form_submit_button("Dodaj")
            if submitted:
                # WYSŁANIE FORMA DO API
                print(date_val, title_val, desc_val, priority_val)
                # ZAMKNIECIE DIALOGU PO KLINIECIU SUBMIT
                st.session_state["show_dialog"] = False
                st.rerun()

    if "choose" not in st.session_state:
        if st.button("Dodaj cel"):
            choose(dt_pl)
    #TODO: add, delete i update modale dla celi
    #TODO: modal do edycji wolnych godzin
    #TODO: modal do ustawien uzytkownika