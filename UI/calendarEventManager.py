import streamlit as st
from datetime import date, datetime
from streamlit_calendar import calendar
import random

#bedzie odpowiadalo za komunikacje z api
def addEvent(name, start, end, group_id):
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    start = str(start)
    end = str(end)
    is_goal = group_id == "goal"
    event ={
        "title": name,
        "groupId": group_id,
        "allDay": is_goal,
        "color": color,
        "start": start,
        "end": end,
    }
    st.session_state["events"].append(event)

def updateEventsInAPI():
    for event in st.session_state.events:
        if event["groupId"] == "goal":
            return
            #TODO: wywolac funkcje co wysle ten cel do api, i wymusić wygenerowanie nowego planu
        getEventsFromAPI() #wczytanie nowego planu

def getEventsFromAPI():
    events = []
    #TODO: pobrać eventy z API
    st.session_state.events = events