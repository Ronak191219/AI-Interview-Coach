import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"
REPORTS_DIR = BASE_DIR / "saved_reports"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = "gemini-2.0-flash"
MODEL_NAME = LLM_MODEL
LLM_TEMPERATURE = 0.7
MAX_INTERVIEW_TURNS = 6