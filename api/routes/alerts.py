from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import Project, Incident, SystemEvent, IncidentStatus
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/hooks", tags=["SRE Gateway"])

class AlertPayload(BaseModel):
    alerts: List[Dict[str, Any]]
    commonLabels: Dict[str, str]

@router.post("/alert")
async def ingest_alert(payload: AlertPayload, db: Session = Depends(get_db)):
    for alert in payload.alerts:
        project_id = alert.get("labels", {}).get("project_id")
        alert_name = alert.get("labels", {}).get("alertname")

        if not project_id:
            # Dead-letter logic for unmapped alerts
            event = SystemEvent(event_type="UNMAPPED_ALERT", payload=alert)
            db.add(event)
            db.commit()
            continue

        incident = Incident(
            project_id=project_id,
            alert_name=alert_name,
            severity=alert.get("labels", {}).get("severity", "info"),
            raw_payload=alert,
            status=IncidentStatus.TRIGGERED
        )
        db.add(incident)
        db.commit()
        # Trigger Async Investigator Task via Celery
        # investigate_task.delay(incident.id)
    return {"status": "accepted"}