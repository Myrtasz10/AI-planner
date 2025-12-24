class TimeSlot:
    def __init__(self, start_time: str, end_time: str, date: str, energy_level: str = "medium"):
        self.start_time = start_time 
        self.end_time = end_time 
        self.date = date  # Format: "YYYY-MM-DD"
        self.energy_level = energy_level  