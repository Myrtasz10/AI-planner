import json
import os

DB_FILE = 'database.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {"events": [], "availability": []}

    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"events": [], "availability": []}


def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=str)


def add_event_to_db(title, start, end, group_id, description="", priority="medium"):
    data = load_db()

    existing_ids = [int(e["id"]) for e in data["events"] if "id" in e and str(e["id"]).isdigit()]
    new_id = max(existing_ids, default=0) + 1

    color = "#FF6C6C" if group_id == "goal" else "#3788d8"

    new_event = {
        "id": str(new_id),
        "title": title,
        "start": str(start),
        "end": str(end),
        "groupId": group_id,
        "allDay": True,
        "color": color,
        "extendedProps": {
            "description": description,
            "priority": priority
        }
    }

    data["events"].append(new_event)
    save_db(data)
    return new_event


def update_event(event_id, new_title=None, new_start=None, new_end=None, new_desc=None):
    data = load_db()
    found = False

    for event in data["events"]:
        if str(event.get("id")) == str(event_id):
            if new_title: event["title"] = new_title
            if new_start: event["start"] = str(new_start)
            if new_end: event["end"] = str(new_end)
            if new_desc: event["extendedProps"]["description"] = new_desc
            found = True
            break

    if found:
        save_db(data)
        return True
    return False


def delete_event(event_id):
    data = load_db()
    original_count = len(data["events"])

    data["events"] = [e for e in data["events"] if str(e.get("id")) != str(event_id)]

    if len(data["events"]) < original_count:
        save_db(data)
        return True
    return False

def get_all_events():
    data = load_db()
    return data.get("events", [])


def get_availability_for_date(target_date):
    data = load_db()
    target_date_str = str(target_date)

    for event in data["events"]:
        if event.get("groupId") == "availability" and event.get("start", "").startswith(target_date_str):
            return event
    return "09:00-17:00"

def get_data_for_ai():
    data = load_db()
    return json.dumps(data, ensure_ascii=False, indent=2)