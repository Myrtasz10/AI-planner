import os
from dotenv import load_dotenv
from AIEngine.GeminiClient import GeminiClient
from AIEngine.PlanValidator import PlanValidator
from AIEngine.DailyPlanManager import DailyPlanManager
from AIEngine.Task import Task
from AIEngine.TimeSlot import TimeSlot
from data_manager import get_goals_for_ai, get_availability_for_ai, save_ai_plan, clear_ai_schedule


def run_ai_scheduler():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"success": False, "message": "Brak klucza API w pliku .env"}

    client = GeminiClient(api_key)
    validator = PlanValidator()
    planner = DailyPlanManager(client, validator)

    # 1. Fetch Goals
    db_goals = get_goals_for_ai()
    if not db_goals:
        return {"success": False, "message": "Brak celów do zaplanowania! Dodaj cel."}

    # 2. Convert Goals to AI Tasks
    ai_tasks = []
    for goal in db_goals:
        props = goal.get("extendedProps", {})
        # Defaults: Medium priority (2) if not set, 60 mins if not set
        prio_map = {"bardzo wazne": 1, "srednio wazne": 2, "malo wazne": 3}
        prio = prio_map.get(props.get("priority"), 2)

        t = Task(
            task_id=goal["id"],
            name=goal["title"],
            description=props.get("description", ""),
            priority=prio,
            estimated_duration_minutes=int(props.get("duration", 60)),
            deadline=goal.get("start"),
            energy_level_required="medium"
        )
        ai_tasks.append(t)

    # 3. Fetch Availability Slots
    db_availability = get_availability_for_ai()
    available_slots = []

    if db_availability:
        for slot in db_availability:
            # slot["start"] is typically ISO string "2024-01-01T09:00:00"
            # We need to extract HH:MM and Date
            try:
                # Simple parsing assuming standard format
                date_part = slot["start"].split("T")[0]
                start_time = slot["start"].split("T")[1][:5]  # HH:MM
                end_time = slot["end"].split("T")[1][:5]  # HH:MM

                available_slots.append(TimeSlot(start_time, end_time, date_part, "high"))
            except:
                continue
    else:
        # FALLBACK: If user didn't set hours, give standard work day
        # This prevents the AI from crashing if the user forgets to set availability
        today = "2024-01-01"
        available_slots = [TimeSlot("09:00", "17:00", today, "medium")]

    # 4. Generate & Save
    try:
        clear_ai_schedule()
        result = planner.generate_plan(ai_tasks, available_slots)

        if result and "schedule" in result:
            save_ai_plan(result["schedule"])
            return {"success": True, "message": result["summary"]["message"]}
        else:
            return {"success": False, "message": "AI nie zwróciło poprawnego harmonogramu."}

    except Exception as e:
        return {"success": False, "message": str(e)}