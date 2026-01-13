Below I've explained how the AI logic has been implemented so it can be used as black-box and external element in the application functionality.

The current `main.py` file shows a preview of how the communication between app and AI layers of application can occur. Contents of this file can be used for testing and as an example, but should be removed later.

The AI integration is waiting for a request called by `planner.generate_plan`. An example usage of this is visible within the `main.py` file in line 88. Some example values of tasks and time slots data have been added in the code but it should be later replaced with data fetched from the database.

Also example JSON values have been included in the examples directory `./AIEngine/examples` for easier reference.

The system tries 3 times to get a valid JSON response from the AI layer. In case of issues it returns a response specified in `_get_fallback_plan` function within `DailyPlanManager` function.

All required packages for this integration have been mentioned in the `requirements.txt` file. Usage of venv is advised.

Please make sure to add `GEMINI_API_KEY` within the `.env` file during development.
