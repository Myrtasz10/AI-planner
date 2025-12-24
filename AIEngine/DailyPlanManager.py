import json
from typing import Dict, List, Any, Optional
from .GeminiClient import GeminiClient
from .PlanValidator import PlanValidator
from .Task import Task
from .TimeSlot import TimeSlot


class DailyPlanManager:
    """Główny orkiestrator - zarządza planowaniem dnia."""
    
    def __init__(self, client: GeminiClient, validator: PlanValidator):
        self.client = client
        self.validator = validator

    def generate_plan(self, 
                     tasks: List[Task], 
                     available_time_slots: List[TimeSlot],
                     max_retries: int = 3) -> Dict[str, Any]:
        
        # prep payload for request
        payload = self._prepare_payload(tasks, available_time_slots)

        print(payload)
        
        for attempt in range(max_retries):
            try:
                raw_response = self.client.ask_for_plan(payload)

                print(f"Attempt {attempt + 1} successful. Result:")

                print(raw_response)
                
                if self.validator.is_valid(raw_response):
                    return self.validator.parse_and_validate(raw_response)
                
            except Exception as e:
                print(f"Error in attempt {attempt + 1}: {str(e)}")
                
            print(f"Retrying...")
        
        return self._get_fallback_plan()

    def _prepare_payload(self, 
                        tasks: List[Task], 
                        time_slots: List[TimeSlot]
                        ) -> str:
        
        tasks_data = []
        for task in tasks:
            task_dict = {
                "task_id": task.task_id,
                "name": task.name,
                "description": task.description,
                "priority": task.priority,
                "estimated_duration_minutes": task.estimated_duration_minutes,
                "deadline": task.deadline,
                "main_goal": task.main_goal,
                "current_stage": task.current_stage,
                "activity_type": task.activity_type,
                "energy_level_required": task.energy_level_required
            }
            tasks_data.append(task_dict)

        slots_data = []
        for slot in time_slots:
            slot_dict = {
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "date": slot.date,
                "energy_level": slot.energy_level
            }
            slots_data.append(slot_dict)

        payload = f"""        
        ZADANIA DO ZAPLANOWANIA:
        {json.dumps(tasks_data, indent=2, ensure_ascii=False)}
        
        DOSTĘPNE SLOTY CZASOWE:
        {json.dumps(slots_data, indent=2, ensure_ascii=False)}
        
        Zaplanuj te zadania optymalnie w dostępnych slotach czasowych. Uwzględnij priorytety, deadliny i poziom energii wymagany dla każdego zadania.
        """
        
        return payload

    def _get_fallback_plan(self) -> Dict[str, Any]:

        # fallback response if AI did not deliver
        return {
            "summary": {
                "total_time_scheduled_minutes": 0,
                "focus_score": 0,
                "scheduled_tasks_count": 0,
                "unscheduled_tasks_count": 0,
                "message": "we're doomed"
            },
            "schedule": [],
            "unscheduled_tasks": [],
            "productivity_tips": [
                "wez kalendarz i długopis w łape"
            ]
        }