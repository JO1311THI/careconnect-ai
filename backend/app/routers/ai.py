from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional


router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)


class SymptomPayload(BaseModel):
    symptoms: str
    vitals_note: Optional[str] = None


class IntakeMessage(BaseModel):
    message: str


@router.post("/diagnosis-assistant")
def ai_diagnosis_assistant(payload: SymptomPayload):
    text = payload.symptoms.lower()

    possible_conditions: List[str] = []
    advice = "This is not medical advice. Please consult a real doctor."

    if "chest pain" in text or "shortness of breath" in text:
        possible_conditions.append("Cardiac issue / emergency – seek urgent care")
    if "fever" in text and "cough" in text:
        possible_conditions.append("Viral or bacterial respiratory infection")
    if "headache" in text and "vomit" in text:
        possible_conditions.append("Migraine or raised intracranial pressure")

    if not possible_conditions:
        possible_conditions.append("General / non-specific illness – further evaluation needed")

    return {
        "possible_conditions": possible_conditions,
        "advice": advice,
    }


@router.post("/intake-chat")
def intake_chat(msg: IntakeMessage):
    text = msg.message.lower()

    if "fever" in text:
        follow_up = "How long have you had the fever and how high has it gone?"
    elif "pain" in text:
        follow_up = "Where is the pain located and how severe is it from 1 to 10?"
    elif "breath" in text:
        follow_up = "Are you short of breath at rest, or only on exertion?"
    else:
        follow_up = "Can you describe your main symptom, when it started, and what makes it better or worse?"

    return {
        "reply": follow_up
    }
