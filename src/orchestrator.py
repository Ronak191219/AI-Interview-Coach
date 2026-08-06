from typing import List
from config import MAX_INTERVIEW_TURNS
from src.llm_client import LLMClient
from src.models import CandidateProfile, TurnRecord, EvaluationResult
from src.agents import InterviewerAgent, EvaluatorAgent, CoachAgent

class InterviewOrchestrator:
    def __init__(self, profile: CandidateProfile):
        self.profile = profile
        self.llm_client = LLMClient()
        self.interviewer = InterviewerAgent(self.llm_client)
        self.evaluator = EvaluatorAgent(self.llm_client)
        self.coach = CoachAgent(self.llm_client)
        self.history: List[TurnRecord] = []

    def start_interview(self) -> str:
        return self.interviewer.generate_opening_question(self.profile)

    def process_turn(self, current_question: str, candidate_response: str) -> EvaluationResult:
        evaluation = self.evaluator.evaluate_response(
            self.profile, current_question, candidate_response
        )
        record = TurnRecord(
            turn_number=len(self.history) + 1,
            interviewer_question=current_question,
            candidate_response=candidate_response,
            evaluation=evaluation
        )
        self.history.append(record)
        return evaluation

    def get_next_question(self) -> str:
        return self.interviewer.generate_next_question(self.profile, self.history)

    def generate_final_report(self) -> str:
        return self.coach.generate_feedback_report(self.profile, self.history)