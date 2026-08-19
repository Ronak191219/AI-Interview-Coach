import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")
MODEL_NAME = LLM_MODEL
LLM_TEMPERATURE = 0.7
MAX_INTERVIEW_TURNS = 6