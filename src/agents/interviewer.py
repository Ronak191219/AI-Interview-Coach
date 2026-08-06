from string import Template
from config import PROMPTS_DIR
from src.llm_client import LLMClient
from src.models import CandidateProfile, TurnRecord
from typing import List

class InterviewerAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        prompt_path = PROMPTS_DIR / "interviewer_agent.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.base_prompt_template = Template(f.read())

    def generate_opening_question(self, profile: CandidateProfile) -> str:
        system_prompt = self.base_prompt_template.safe_substitute(
            target_role=profile.target_role,
            candidate_background=profile.candidate_background,
            focus_area=profile.focus_area
        )
        user_prompt = "Start the interview now. Welcome the candidate briefly and ask your opening question."
        return self.llm_client.generate(system_prompt, user_prompt)

    def generate_next_question(
        self,
        profile: CandidateProfile,
        history: List[TurnRecord]
    ) -> str:
        system_prompt = self.base_prompt_template.safe_substitute(
            target_role=profile.target_role,
            candidate_background=profile.candidate_background,
            focus_area=profile.focus_area
        )

        formatted_history = ""
        for turn in history:
            formatted_history += f"Turn {turn.turn_number}:\n"
            formatted_history += f"Interviewer: {turn.interviewer_question}\n"
            formatted_history += f"Candidate: {turn.candidate_response}\n"
            formatted_history += f"Evaluator Feedback: Suggested Action - {turn.evaluation.suggested_next_action}, Quality - {turn.evaluation.overall_quality}\n\n"

        user_prompt = (
            f"Here is the interview progress so far:\n\n{formatted_history}\n"
            f"Based on the latest evaluation and response, generate the next interview turn (Question {len(history) + 1})."
        )
        return self.llm_client.generate(system_prompt, user_prompt)