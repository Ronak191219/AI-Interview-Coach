import os
import time
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

class LLMClient:
    def __init__(self):
        # 1. API Key fetch karna (Secrets -> Env)
        api_key = None
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass

        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY nahi mili. Streamlit Secrets ya .env check karein.")

        # 2. Model Name fetch karna
        self.model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
        self.client = genai.Client(api_key=api_key)

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                    ),
                )
                return response.text
            except (ClientError, ServerError) as e:
                if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "503" in str(e)) and attempt < max_retries - 1:
                    time.sleep(4 * (attempt + 1))
                else:
                    raise e
            except Exception as e:
                raise e

    def generate_json(self, system_prompt: str, user_prompt: str, response_schema=None) -> str:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                config_args = {
                    "system_instruction": system_prompt,
                    "response_mime_type": "application/json",
                }
                if response_schema:
                    config_args["response_schema"] = response_schema

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(**config_args),
                )
                return response.text
            except (ClientError, ServerError) as e:
                if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "503" in str(e)) and attempt < max_retries - 1:
                    time.sleep(4 * (attempt + 1))
                else:
                    raise e
            except Exception as e:
                raise e