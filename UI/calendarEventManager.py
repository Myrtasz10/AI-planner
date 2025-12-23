import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_manager import add_event_to_db

def addEvent(name, start, end, group_id, description="", priority="medium"):

    add_event_to_db(name, start, end, group_id, description, priority)
    st.rerun()