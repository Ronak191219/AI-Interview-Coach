# from typing import List, Literal
# from pydantic import BaseModel, Field

# class CandidateProfile(BaseModel):
#     target_role: str
#     candidate_background: str = "Not provided"
#     focus_area: Literal["behavioral", "technical", "case", "mixed"] = "mixed"

# class EvaluationResult(BaseModel):
#     technical_accuracy: int = Field(ge=0, le=10, description="Score from 0 to 10")
#     communication_clarity: int = Field(ge=0, le=10, description="Score from 0 to 10")
#     depth_of_reasoning: int = Field(ge=0, le=10, description="Score from 0 to 10")
#     relevance_to_role: int = Field(ge=0, le=10, description="Score from 0 to 10")
#     overall_quality: Literal["strong", "satisfactory", "weak", "evasive/off-topic"]
#     strengths: List[str]
#     weaknesses: List[str]
#     suggested_next_action: Literal["probe_deeper", "pivot", "advance"]
#     brief_justification: str

# class TurnRecord(BaseModel):
#     turn_number: int
#     interviewer_question: str
#     candidate_response: str
#     evaluation: EvaluationResult






from typing import List, Literal
from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    candidate_name: str = "Candidate"
    target_role: str
    candidate_background: str = "Not provided"
    focus_area: Literal["behavioral", "technical", "case", "mixed"] = "mixed"

class EvaluationResult(BaseModel):
    technical_accuracy: int = Field(ge=0, le=10, description="Score from 0 to 10")
    communication_clarity: int = Field(ge=0, le=10, description="Score from 0 to 10")
    depth_of_reasoning: int = Field(ge=0, le=10, description="Score from 0 to 10")
    relevance_to_role: int = Field(ge=0, le=10, description="Score from 0 to 10")
    overall_quality: Literal["strong", "satisfactory", "weak", "evasive/off-topic"]
    strengths: List[str]
    weaknesses: List[str]
    suggested_next_action: Literal["probe_deeper", "pivot", "advance"]
    brief_justification: str

class TurnRecord(BaseModel):
    turn_number: int
    interviewer_question: str
    candidate_response: str
    evaluation: EvaluationResult