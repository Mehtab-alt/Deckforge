from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import engine, Base, get_db
from core.models import Project
from worker.tasks import forge_infrastructure, learn_from_feedback
from api.auth import get_current_user, require_architect
from api.routes.alerts import router as alerts_router
from api.slack_bot import router as slack_router
from pydantic import BaseModel

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the new routes
app.include_router(alerts_router)
app.include_router(slack_router)

class ForgeRequest(BaseModel):
    idea: str
    project_name: str

@app.post("/forge")
def trigger_forge(
    req: ForgeRequest,
    user = Depends(require_architect), # Phase 6 RBAC
    db: Session = Depends(get_db)
):
    # Create Project Entry
    proj_id = req.project_name # uuid in prod
    new_proj = Project(id=proj_id, name=req.project_name, organization_id=user.organization_id)
    db.add(new_proj)
    db.commit()

    # Trigger Phase 7 Worker
    task = forge_infrastructure.delay(proj_id, req.idea, "thread-1")
    return {"task_id": task.id, "status": "queued"}

@app.post("/feedback")
def submit_feedback(
    original: str,
    corrected: str,
    user = Depends(get_current_user)
):
    # Phase 8 Flywheel
    learn_from_feedback.delay(original, corrected)
    return {"status": "Learned"}