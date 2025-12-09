import pytz
import streamlit as st
from datetime import date, datetime
from streamlit_calendar import calendar
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Demo for streamlit-calendar", page_icon="📆")



events = [
    {
        "title": "Event 1",
        "color": "#FF6C6C",
        "start": "2025-12-01",
        "end": "2025-12-11",
    },
]

calendar_options = {
    "navLinks": "true",
    "selectable": "true",
    "height": "auto",
    "contentHeight": "auto",
    "expandsRows": "true",
"headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridDay,dayGridWeek,dayGridMonth",
    },
    "initialDate": date.today().isoformat(),
    "initialView": "dayGridMonth",
}


state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
)

dt = datetime.now()
dt_pl = datetime.now()

if state and "dateClick" in state:
        dt = datetime.fromisoformat(state["dateClick"]["date"])
        dt_pl = dt.astimezone(ZoneInfo("Europe/Warsaw"))

@st.dialog("Wybierz cel")
def choose(choosendate):
    with st.form("goal"):
        date_val = st.date_input("Deadline:", choosendate.date())
        title_val = st.text_input("Nazwa:", "Nazwij swoj cel")
        desc_val = st.text_input("Opis:", "Opisz swoj cel")
        priority_val = st.selectbox("Priorytet", ["malo wazne", "srednio wazne", "bardzo wazne"])
        submitted = st.form_submit_button("Dodaj")
        if submitted:
#WYSŁANIE FORMA DO API
            print(date_val, title_val, desc_val, priority_val)

if "choose" not in st.session_state:
    if st.button("Dodaj cel"):
        choose(dt_pl)
