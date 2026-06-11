from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import List

class IncidentResponse(BaseModel):
    incident_id: str = Field(..., description="Unique identifier for the incident")
    title: str = Field(..., description="Short, descriptive title of the failure point")
    severity: str = Field(..., description="Low, Medium, High, or Critical")
    priority_score: int = Field(..., description="Calculated urgency metric between 0 and 100")
    summary: str = Field(..., description="Concise analysis of what went wrong")
    evidence: List[str] = Field(..., description="Key telemetry fragments backing the claim")
    recommended_action: str = Field(..., description="Immediate next steps for the operator")
    confidence: float = Field(..., description="Model confidence score between 0.0 and 1.0")

# 2. Declare the agent engine natively
signal_shield_agent = Agent(
    name="SignalShield_Core_Triager",
    model="gemini-2.5-flash", 
    instruction=(
        "You are an enterprise triage engine. Ingest raw telemetry blocks, "
        "group related failures, calculate an impact score, and generate "
        "clear, programmatic action items."
    ),
    output_schema=IncidentResponse
)