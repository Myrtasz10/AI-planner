import sys
import os
import streamlit as st
from datetime import date, datetime
from streamlit_calendar import calendar
from UI.modals import runModals

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_manager import get_all_events

def runCalendarView() -> None:
    st.set_page_config(page_title="Demo for streamlit-calendar", page_icon="📆")

    events = events = get_all_events()

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
        events=events,
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

