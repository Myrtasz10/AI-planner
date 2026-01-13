import google.generativeai as genai
from .AIConfig import AIConfig
import json

class GeminiClient:
    """Obsługuje niskopoziomową komunikację z Google API."""
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)               
        
        self.model = genai.GenerativeModel(
            model_name=AIConfig.MODEL_NAME,
            generation_config=AIConfig.get_generation_config(),
            system_instruction=AIConfig.SYSTEM_PROMPT  
        )

    def ask_for_plan(self, user_input: str) -> str:
        try:
            prompt = f"{AIConfig.SYSTEM_PROMPT}\n\n{user_input}"
            response = self.model.generate_content(prompt)
                        

            response_text = response.text.strip()
            
            if response_text and '{' in response_text and '}' in response_text:
                return response_text
            else:
                raise Exception("Invalid response format")
                
        except Exception as e:
            print(f"Error in Gemini API call: {str(e)}")
            raise e