import os
import sys
import json
from typing import List
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from agent.triager import IncidentResponse
from fastapi import FastAPI, HTTPException

app = FastAPI(title="SignalShield Triage Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # need to adjust this to your specific frontend port later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to locate your sample_data directory relative to this backend script
SAMPLE_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_data", "scenario_1_latency.json"))

@app.get("/api/incidents", response_model=IncidentResponse)
def get_triaged_incident():
    """
    Reads raw telemetry data from Scenario 1, passes it to the Gemini reasoning 
    agent, and returns a structured, prioritized incident contract.
    """
    # Verify the mock telemetry payload exists locally
    if not os.path.exists(SAMPLE_DATA_PATH):
        raise HTTPException(
            status_code=404, 
            detail=f"Mock data file missing at {SAMPLE_DATA_PATH}. Please verify Step 3 is complete."
        )
    
    try:
        # Load the messy telemetry file
        with open(SAMPLE_DATA_PATH, "r") as file:
            raw_telemetry = json.load(file)
            
        # ====================================================================
        # PLACEHOLDER: This is where you pass data block straight to the agent 
        # via the platform's execution SDK.
        # ====================================================================
        # From google import genai
        # client = genai.Client()
        # response = client.models.generate_content(
        #     model='gemini-2.5-flash', # Or your specific studio agent deployment ID
        #     contents=f"Triage this telemetry: {json.dumps(raw_telemetry)}",
        #     config={'response_mime_type': 'application/json', 'response_schema': IncidentResponse}
        # )
        # return json.loads(response.text)
        
        # Temporary Mock Fallback matching the explicit contract until SDK keys are live:
        mock_triaged_output = {
            "incident_id": "inc-001",
            "title": "Auth validation tool bottleneck causing systemic latency",
            "severity": "high",
            "priority_score": 87,
            "summary": f"Analyzed runtime metadata from {raw_telemetry.get('workflow_name', 'Unknown Pipeline')}. Timeouts in downstream dependencies caused cascading multi-second delays.",
            "evidence": raw_telemetry.get("error_logs", ["No log fragments captured."]),
            "recommended_action": "Check upstream network health for dependency 'AuthValidationTool' and apply circuit-breaker filters.",
            "confidence": 0.92
        }
        
        return mock_triaged_output

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run the server locally on port 8080
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)