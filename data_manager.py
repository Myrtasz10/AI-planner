import json
import os
from datetime import datetime

DB_FILE = 'database.json'


def load_db():
    if not os.path.exists(DB_FILE):
        # Initialize with separate event groups for clarity
        return {"events": []}
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"events": []}


def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=str)


# Updated to include Duration
def add_event_to_db(title, start, end, group_id, description="", priority="medium", duration=60):
    data = load_db()

    # Simple ID generation
    existing_ids = [int(e["id"]) for e in data["events"] if "id" in e and str(e["id"]).isdigit()]
    new_id = max(existing_ids, default=0) + 1

    # Colors: Goals (Red), AI Work Blocks (Blue), Availability (Green)
    color_map = {"goal": "#FF6C6C", "ai_work": "#3788d8", "availability": "#28a745"}
    color = color_map.get(group_id, "#3788d8")

    new_event = {
        "id": str(new_id),
        "title": title,
        "start": str(start),
        "end": str(end),
        "groupId": group_id,
        "allDay": True if group_id == "goal" else False,
        "color": color,
        "extendedProps": {
            "description": description,
            "priority": priority,
            "duration": duration
        }
    }

    data["events"].append(new_event)
    save_db(data)
    return new_event


def get_all_events():
    data = load_db()
    return data.get("events", [])


def get_goals_for_ai():
    """Returns only user goals that need scheduling"""
    data = load_db()
    return [e for e in data["events"] if e.get("groupId") == "goal"]


def clear_ai_schedule():
    """Removes old AI generated blocks before creating a new plan"""
    data = load_db()
    # Keep goals, delete ai_work
    data["events"] = [e for e in data["events"] if e.get("groupId") != "ai_work"]
    save_db(data)


def save_ai_plan(ai_schedule_list):
    """Takes the list of dictionaries from AI response and saves to DB"""
    data = load_db()

    # Calculate next ID
    existing_ids = [int(e["id"]) for e in data["events"] if "id" in e and str(e["id"]).isdigit()]
    next_id = max(existing_ids, default=0) + 1

    today_str = datetime.now().strftime("%Y-%m-%d")

    for item in ai_schedule_list:
        # Convert HH:MM to full ISO string for the calendar
        start_iso = f"{today_str}T{item['start_time']}:00"
        end_iso = f"{today_str}T{item['end_time']}:00"

        new_event = {
            "id": str(next_id),
            "title": item['task_name'],
            "start": start_iso,
            "end": end_iso,
            "groupId": "ai_work",
            "allDay": False,
            "color": "#3788d8",
            "extendedProps": {
                "description": item.get('description', ''),
                "priority": item.get('priority', 2),
                "energy": item.get('energy_level_required', 'medium')
            }
        }
        data["events"].append(new_event)
        next_id += 1

    save_db(data)