import streamlit as st
from datetime import date, datetime
from streamlit_calendar import calendar
from UI.modals import runModals
from UI.calendarEventManager import getEventsFromAPI

def runCalendarView() -> None:
    st.set_page_config(page_title="AI Planner", page_icon="📆")

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
        "height": "600px",
        "contentHeight": "-webkit-fill-available",
        "expandsRows": "true",
        "slotMinTime": "00:00:00",
        "slotMaxTime": "23:59:59",
        "allDaySlot": "true",
    "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "timeGridDay,dayGridWeek,dayGridMonth",
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

    if "events" not in st.session_state:
        st.session_state["events"] = events
        #TODO: po polaczeniu z api dodać getEventsFromAPI()

    runModals(state)

