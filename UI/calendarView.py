import streamlit as st
from datetime import date, datetime
from streamlit_calendar import calendar
from UI.modals import runModals

def runCalendarView() -> None:
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
        "slotMinTime": "00:00:00",
        "slotMaxTime": "23:59:59",
        "allDaySlot": False,
    "headerToolbar": {
            "left": "prev,today,next",
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

    runModals(state)

