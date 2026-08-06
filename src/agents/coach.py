from string import Template
from config import PROMPTS_DIR
from src.llm_client import LLMClient
from src.models import CandidateProfile, TurnRecord
from typing import List

class CoachAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        prompt_path = PROMPTS_DIR / "coach_agent.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.base_prompt_template = Template(f.read())

    def generate_feedback_report(
        self,
        profile: CandidateProfile,
        history: List[TurnRecord]
    ) -> str:
        system_prompt = self.base_prompt_template.safe_substitute(
            candidate_name=profile.candidate_name,
            target_role=profile.target_role,
            focus_area=profile.focus_area
        )

        full_transcript = ""
        for turn in history:
            full_transcript += f"### Turn {turn.turn_number}\n"
            full_transcript += f"**Interviewer Question:** {turn.interviewer_question}\n\n"
            full_transcript += f"**Candidate Response:** {turn.candidate_response}\n\n"
            full_transcript += f"**Evaluator Scores:** Tech: {turn.evaluation.technical_accuracy}/10 | Clarity: {turn.evaluation.communication_clarity}/10 | Depth: {turn.evaluation.depth_of_reasoning}/10 | Role Fit: {turn.evaluation.relevance_to_role}/10\n"
            full_transcript += f"**Evaluator Action:** {turn.evaluation.suggested_next_action}\n"
            full_transcript += f"**Evaluator Notes:** {turn.evaluation.brief_justification}\n\n"
            full_transcript += "---\n\n"

        user_prompt = f"Candidate Name: {profile.candidate_name}\nTarget Role: {profile.target_role}\n\nSynthesize the complete interview history into the final report:\n\n{full_transcript}"
        return self.llm_client.generate(system_prompt, user_prompt)