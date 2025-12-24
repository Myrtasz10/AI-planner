from typing import Optional

class Task:
    def __init__(self, 
                 task_id: str,
                 name: str,
                 description: str = "",
                 priority: int = 3,
                 estimated_duration_minutes: int = 60,
                 deadline: Optional[str] = None,
                 main_goal: str = "",
                 current_stage: str = "",
                 activity_type: str = "work",
                 energy_level_required: str = "medium"):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.priority = priority 
        self.estimated_duration_minutes = estimated_duration_minutes
        self.deadline = deadline 
        self.main_goal = main_goal
        self.current_stage = current_stage
        self.activity_type = activity_type  # "work", "meeting", "break", "personal"
        self.energy_level_required = energy_level_required  # "low", "medium", "high"
