import os
import hmac
import hashlib
import time
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import Incident, IncidentStatus
from worker.tasks import execute_remediation
import json

router = APIRouter(prefix="/slack", tags=["ChatOps"])
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

async def verify_slack_signature(request: Request, x_slack_signature: str, x_slack_request_timestamp: str):
    """Harden security: Verify that requests actually come from Slack."""
    if abs(time.time() - int(x_slack_request_timestamp)) > 60 * 5:
        raise HTTPException(status_code=403, detail="Timestamp expired")
    
    body = await request.body()
    sig_basestring = f"v0:{x_slack_request_timestamp}:{body.decode()}"
    my_sig = "v0=" + hmac.new(SLACK_SIGNING_SECRET.encode(), sig_basestring.encode(), hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(my_sig, x_slack_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")


class SlackInteractionPayload(BaseModel):
    type: str
    actions: list
    callback_id: str
    team: Dict[str, str]
    user: Dict[str, str]
    channel: Dict[str, str]
    response_url: str
    trigger_id: str
    message_ts: str
    attachment_id: str
    token: str
    original_message: Dict[str, Any]


@router.post("/interactive")
async def handle_interaction(
    request: Request,
    x_slack_signature: str = Header(None),
    x_slack_request_timestamp: str = Header(None),
    db: Session = Depends(get_db)
):
    await verify_slack_signature(request, x_slack_signature, x_slack_request_timestamp)

    # Parse the form-encoded payload
    form_data = await request.form()
    payload_str = form_data.get("payload", "{}")
    payload = json.loads(payload_str)

    # Extract incident ID and remediation details from the callback
    callback_id = payload.get("callback_id", "")
    if callback_id.startswith("remediate_"):
        parts = callback_id.split("_")
        if len(parts) >= 3:
            incident_id = parts[1]
            playbook_name = parts[2] if len(parts) > 2 else "restart_service"
            
            # Get additional parameters from the action values
            actions = payload.get("actions", [])
            target_ip = "127.0.0.1"  # Default fallback
            params = {}
            
            for action in actions:
                if action.get("type") == "button" and "value" in action:
                    # Extract target IP and other parameters from action value
                    # In a real implementation, this would be structured differently
                    pass

            # Update incident status to EXECUTING
            incident = db.query(Incident).filter(Incident.id == incident_id).first()
            if incident:
                incident.status = IncidentStatus.EXECUTING
                db.commit()

                # Trigger the remediation task asynchronously
                execute_remediation.delay(
                    incident_id=incident_id,
                    target_ip=target_ip,
                    playbook_name=playbook_name,
                    params=params
                )

    return {"text": "Remediation Approved. Executing via DeckForge Worker..."}


@router.post("/events")
async def handle_events(
    request: Request,
    x_slack_signature: str = Header(None), 
    x_slack_request_timestamp: str = Header(None)
):
    """Handle Slack events like app installation, messages, etc."""
    await verify_slack_signature(request, x_slack_signature, x_slack_request_timestamp)
    
    payload = await request.json()
    
    if payload.get("type") == "url_verification":
        # Respond to Slack challenge
        return {"challenge": payload.get("challenge")}
    
    return {"status": "received"}