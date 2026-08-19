import os
import time
import json
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError
from config import GEMINI_API_KEY, LLM_MODEL

class LLMClient:
    def __init__(self):
        # 1. Load API Key safely
        api_key = None
        try:
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass

        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY") or GEMINI_API_KEY

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in Streamlit Secrets or Environment Variables.")

        # 2. Assign attributes
        self.model = LLM_MODEL or "gemini-1.5-flash"
        self.model_name = self.model
        self.client = genai.Client(api_key=api_key)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Text generation with retry mechanism."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.7,
                    ),
                )
                return response.text.strip()
            except (ClientError, ServerError) as e:
                if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "503" in str(e)) and attempt < max_retries - 1:
                    time.sleep(4 * (attempt + 1))
                else:
                    raise e
            except Exception as e:
                raise e

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        return self.generate(system_prompt, user_prompt)

    def generate_json(self, system_prompt: str, user_prompt: str, response_schema=None) -> str:
        """JSON output generation with retry mechanism."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                config_args = {
                    "system_instruction": system_prompt,
                    "response_mime_type": "application/json",
                    "temperature": 0.2,
                }
                if response_schema:
                    config_args["response_schema"] = response_schema

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(**config_args),
                )
                return response.text.strip()
            except (ClientError, ServerError) as e:
                if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "503" in str(e)) and attempt < max_retries - 1:
                    time.sleep(4 * (attempt + 1))
                else:
                    raise e
            except Exception as e:
                raise e