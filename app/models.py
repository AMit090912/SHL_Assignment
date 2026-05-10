from pydantic import BaseModel
from typing import List


class Assessment(BaseModel):
    entity_id: str
    name: str
    url: str
    description: str

    job_levels: List[str] = []
    languages: List[str] = []
    duration: str = ""

    remote: bool = False
    adaptive: bool = False

    categories: List[str] = []


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool

class ConversationState(BaseModel):

    role: str | None = None
    seniority: str | None = None

    skills: List[str] = []

    needs_technical: bool = False
    needs_personality: bool = False
    needs_cognitive: bool = False

    communication_required: bool = False
    leadership_required: bool = False

    ready_for_recommendation: bool = False

