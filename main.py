import os
from dotenv import load_dotenv
from AIEngine.GeminiClient import GeminiClient
from AIEngine.PlanValidator import PlanValidator
from AIEngine.DailyPlanManager import DailyPlanManager
from AIEngine.Task import Task
from AIEngine.TimeSlot import TimeSlot
from UI.calendarView import runCalendarView

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
    
    runCalendarView()

if __name__ == "__main__":
    main()