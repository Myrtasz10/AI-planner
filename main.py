import os
from dotenv import load_dotenv
from AIEngine.GeminiClient import GeminiClient
from AIEngine.PlanValidator import PlanValidator
from AIEngine.DailyPlanManager import DailyPlanManager
from AIEngine.Task import Task
from AIEngine.TimeSlot import TimeSlot

def main():
    
    # env
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("api key not found")
        return
    
    # init
    client = GeminiClient(api_key)
    validator = PlanValidator()
    planner = DailyPlanManager(client, validator)
    
    # example tasks
    sample_tasks = [
        Task(
            task_id="1",
            name="Przygotowanie prezentacji",
            description="Przygotowanie prezentacji na spotkanie zespołowe",
            priority=1,
            estimated_duration_minutes=360,
            deadline="2024-12-20 14:00",
            main_goal="Przedstawienie wyników projektu",
            activity_type="work",
            energy_level_required="high"
        ),
        Task(
            task_id="2",
            name="Code review",
            description="Przegląd kodu w projekcie XYZ",
            priority=2,
            estimated_duration_minutes=60,
            deadline="2024-12-20",
            main_goal="Zapewnienie jakości kodu",
            activity_type="work",
            energy_level_required="medium"
        ),
        Task(
            task_id="3",
            name="Spotkanie z klientem",
            description="Omówienie wymagań projektu",
            priority=1,
            estimated_duration_minutes=60,
            deadline="2024-12-20 16:00",
            main_goal="Ustalenie wymagań",
            activity_type="meeting",
            energy_level_required="medium"
        ),
        Task(
            task_id="4",
            name="Odpowiedź na emaile",
            description="Przejrzenie i odpowiedź na ważne emaile",
            priority=3,
            estimated_duration_minutes=30,
            main_goal="Komunikacja z zespołem",
            activity_type="work",
            energy_level_required="low"
        )
    ]
    
    # example timeslots
    time_slots = [
        TimeSlot("09:00", "12:00", "2024-12-20", "high"),  
        TimeSlot("13:00", "15:00", "2024-12-20", "medium"),  
        TimeSlot("15:30", "17:00", "2024-12-20", "medium"),  
        TimeSlot("19:00", "21:00", "2024-12-20", "low")      
    ]
    
    print("Generating plan...")
    

    try:

        # AI CALL
        plan = planner.generate_plan(sample_tasks, time_slots)
        print(plan)
        
    except Exception as e:
        print(f"Error while generating plan: {str(e)}")


if __name__ == "__main__":
    main()