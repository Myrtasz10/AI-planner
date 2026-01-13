import os
from dotenv import load_dotenv
from AIEngine.GeminiClient import GeminiClient
from AIEngine.PlanValidator import PlanValidator
from AIEngine.DailyPlanManager import DailyPlanManager
from AIEngine.Task import Task
from AIEngine.TimeSlot import TimeSlot
from data_manager import get_goals_for_ai, save_ai_plan, clear_ai_schedule


def run_ai_scheduler():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"success": False, "message": "API Key missing"}

    # 1. Initialize AI
    client = GeminiClient(api_key)
    validator = PlanValidator()
    planner = DailyPlanManager(client, validator)

    # 2. Fetch Data from DB
    db_goals = get_goals_for_ai()

    if not db_goals:
        return {"success": False, "message": "No goals found to plan!"}

    # 3. Convert DB Goals -> AI Tasks
    ai_tasks = []
    for goal in db_goals:
        props = goal.get("extendedProps", {})

        # Mapping DB fields to Task object
        t = Task(
            task_id=goal["id"],
            name=goal["title"],
            description=props.get("description", ""),
            priority=convert_priority(props.get("priority", "medium")),
            estimated_duration_minutes=int(props.get("duration", 60)),  # Now using duration
            deadline=goal.get("start"),  # Using the goal date as deadline
            energy_level_required="medium"  # Defaulting for now
        )
        ai_tasks.append(t)

    # 4. Define Available Time Slots (Hardcoded for "Simple App" scope)
    # Ideally this comes from the "Free Hours" modal in DB
    today = "2024-01-01"  # Date doesn't strictly matter for the AI logic processing time
    available_slots = [
        TimeSlot("09:00", "13:00", today, "high"),
        TimeSlot("14:00", "18:00", today, "medium")
    ]

    # 5. Run Generation
    try:
        # Clear old plan first
        clear_ai_schedule()

        result = planner.generate_plan(ai_tasks, available_slots)

        # 6. Save result back to DB
        if result and "schedule" in result:
            save_ai_plan(result["schedule"])
            return {"success": True, "message": result["summary"]["message"]}
        else:
            return {"success": False, "message": "AI failed to generate a valid schedule."}

    except Exception as e:
        return {"success": False, "message": str(e)}


def convert_priority(p_str):
    if "bardzo" in p_str or "high" in p_str: return 1
    if "srednio" in p_str or "medium" in p_str: return 2
    return 3