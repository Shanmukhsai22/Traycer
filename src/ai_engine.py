import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = 'gemini-1.0-pro'

class AIEngine:
    def __init__(self):
        # Use provided API key or fall back to config
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key must be provided")
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(MODEL_NAME)
        except Exception as e:
            raise Exception(f"Gemini API Configuration Error: {str(e)}")

    def generate_response(self, prompt: str) -> str:
        """Generate AI response using Gemini API."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"AI Engine Error: {str(e)}")

    def analyze_code(self, code: str) -> dict:
        """Analyze code snippet and provide insights."""
        prompt = f"""
        Analyze the following code and provide insights about:
        1. Purpose and functionality
        2. Code quality
        3. Potential improvements
        
        Code:
        ```
        {code}
        ```
        """
        response = self.generate_response(prompt)
        return self._parse_code_analysis(response)

    def _parse_code_analysis(self, response: str) -> dict:
        """Parse AI response into structured code analysis."""
        sections = response.split('\n\n')
        analysis = {
            'purpose': '',
            'quality': '',
            'improvements': []
        }
        
        for section in sections:
            if 'purpose' in section.lower():
                analysis['purpose'] = section
            elif 'quality' in section.lower():
                analysis['quality'] = section
            elif 'improvement' in section.lower():
                improvements = section.split('\n')[1:]
                analysis['improvements'] = [imp.strip('- ') for imp in improvements]
                
        return analysis