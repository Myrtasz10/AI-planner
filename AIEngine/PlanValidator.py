import json
from typing import Dict, Any

class PlanValidator:
    REQUIRED_KEYS = ["summary", "schedule", "unscheduled_tasks"]
    REQUIRED_SUMMARY_KEYS = ["total_time_scheduled_minutes", "focus_score", "message"]
    REQUIRED_SCHEDULE_KEYS = ["start_time", "end_time", "task_name", "activity_type"]

    def is_valid(self, raw_data: str) -> bool:
        
        # try to parse to json
        try:
            data = json.loads(raw_data)
            return self._validate_structure(data)
        except json.JSONDecodeError:
            return False

    def _validate_structure(self, data: Dict[Any, Any]) -> bool:
        

        # validate if response JSON has all required keys
        if not all(key in data for key in self.REQUIRED_KEYS):
            return False
        
        summary = data.get("summary", {})
        if not all(key in summary for key in self.REQUIRED_SUMMARY_KEYS):
            return False
        
        schedule = data.get("schedule", [])
        if not isinstance(schedule, list):
            return False
        
        for item in schedule:
            if not all(key in item for key in self.REQUIRED_SCHEDULE_KEYS):
                return False
        
        return True

    def parse_and_validate(self, raw_data: str) -> Dict[Any, Any]:
        
        # main function for external call
        if not self.is_valid(raw_data):
            raise ValueError("Invalid response structure from AI")
        
        return json.loads(raw_data)