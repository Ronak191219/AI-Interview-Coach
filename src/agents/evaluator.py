# import json
# from config import PROMPTS_DIR
# from src.llm_client import LLMClient
# from src.models import CandidateProfile, EvaluationResult

# class EvaluatorAgent:
#     def __init__(self, llm_client: LLMClient):
#         self.llm_client = llm_client
#         prompt_path = PROMPTS_DIR / "evaluator_agent.txt"
#         with open(prompt_path, "r", encoding="utf-8") as f:
#             self.base_prompt_template = f.read()

#     def evaluate_response(
#         self,
#         profile: CandidateProfile,
#         question: str,
#         candidate_response: str
#     ) -> EvaluationResult:
#         system_prompt = self.base_prompt_template.format(
#             target_role=profile.target_role,
#             focus_area=profile.focus_area,
#             question=question,
#             response=candidate_response
#         )
#         user_prompt = "Evaluate the candidate's response."
        
#         # Pass EvaluationResult schema to Gemini Client
#         raw_json = self.llm_client.generate_json(system_prompt, user_prompt, response_schema=EvaluationResult)
#         parsed_data = json.loads(raw_json)
#         return EvaluationResult(**parsed_data)










import json
from string import Template
from config import PROMPTS_DIR
from src.llm_client import LLMClient
from src.models import CandidateProfile, EvaluationResult

class EvaluatorAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        prompt_path = PROMPTS_DIR / "evaluator_agent.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.base_prompt_template = Template(f.read())

    def evaluate_response(
        self,
        profile: CandidateProfile,
        question: str,
        candidate_response: str
    ) -> EvaluationResult:
        system_prompt = self.base_prompt_template.safe_substitute(
            target_role=profile.target_role,
            focus_area=profile.focus_area,
            question=question,
            response=candidate_response
        )
        user_prompt = "Evaluate the candidate's response."
        
        raw_json = self.llm_client.generate_json(system_prompt, user_prompt, response_schema=EvaluationResult)
        parsed_data = json.loads(raw_json)
        return EvaluationResult(**parsed_data)