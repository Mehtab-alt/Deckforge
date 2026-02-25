import os
from celery import Celery
from core.database import SessionLocal
from core.models import Project, TrainingData, Incident, IncidentStatus
from core.state_parser import StateParser
# Import your Phase 1-4 Logic
from agents.orchestrator import brain
from core.schema import AgentState
import ansible_runner

REDIS_URL = os.getenv("REDIS_URL")
celery_app = Celery("deckforge", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(bind=True)
def forge_infrastructure(self, project_id: str, idea: str, thread_id: str):
    """
    Phase 7: Long-running generation task.
    """
    # 1. Init State
    state = AgentState(thread_id=thread_id, user_idea=idea)
    
    # 2. Run LangGraph
    final_state = brain.invoke(state)
    
    # 3. Save Artifacts to Disk (Shared Volume)
    export_path = f"/app/exports/{project_id}"
    os.makedirs(export_path, exist_ok=True)
    # ... logic to write state.artifacts to export_path ...
    
    return {
        "status": "COMPLETED",
        "artifacts": final_state['artifacts'],
        "path": export_path
    }

@celery_app.task
def detect_drift(project_id: str):
    """
    Phase 5: Scheduled task to check state.
    """
    db = SessionLocal()
    path = f"/app/exports/{project_id}"
    parser = StateParser(path)
    resources = parser.get_live_resources()
    
    # Simple drift logic: If resource count changed dramatically or status is 'terminated'
    # In real world: Compare with Plan
    
    project = db.query(Project).filter(Project.id == project_id).first()
    # Update DB with resource health
    db.close()
    return resources

@celery_app.task
def learn_from_feedback(original: str, corrected: str):
    """
    Phase 8: The Flywheel.
    """
    db = SessionLocal()
    data = TrainingData(original_ai_output=original, human_corrected_output=corrected)
    db.add(data)
    db.commit()
    db.close()

@celery_app.task
def execute_remediation(incident_id: str, target_ip: str, playbook_name: str, params: dict):
    """
    Phase 9: Execute verified remediation via ansible-runner.
    """
    db = SessionLocal()
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    # Execute using ansible-runner for process isolation and callbacks
    r = ansible_runner.run(
        private_data_dir='/tmp/ansible',
        playbook=f'templates/runbooks/{playbook_name}.yml',
        inventory=f'{target_ip},',
        extravars=params
    )

    incident.status = IncidentStatus.RESOLVED if r.rc == 0 else IncidentStatus.FAILED
    incident.remediation_log = r.stdout.read()
    db.commit()
    db.close()