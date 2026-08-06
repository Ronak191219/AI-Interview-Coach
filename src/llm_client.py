import sys
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, LLM_MODEL, LLM_TEMPERATURE

class LLMClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in your .env file.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = LLM_MODEL

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = LLM_TEMPERATURE) -> str:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=config,
            )
            return response.text.strip()
        except Exception as e:
            print(f"[Gemini API Error]: {e}")
            raise e

    def generate_json(self, system_prompt: str, user_prompt: str, response_schema) -> str:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=response_schema
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=config,
            )
            return response.text.strip()
        except Exception as e:
            print(f"[Gemini Structured Output Error]: {e}")
            raise e