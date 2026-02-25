from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Float, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
import uuid
from core.database import Base

class IncidentStatus(str, enum.Enum):
    TRIGGERED = "triggered"
    INVESTIGATING = "investigating"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    RESOLVED = "resolved"
    FAILED = "failed"
    UNMAPPED = "unmapped" # Dead-letter status

class RemediationPolicy(Base):
    __tablename__ = "remediation_policies"
    id = Column(Integer, primary_key=True)
    organization_id = Column(String, ForeignKey("organizations.id"))
    alert_name = Column(String, index=True)
    allowed_actions = Column(JSON, default=[]) # e.g., ["clear_tmp", "restart_service"]
    requires_approval = Column(Boolean, default=True)
    max_cost_impact = Column(Float, default=0.0)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.TRIGGERED)
    severity = Column(String)
    alert_name = Column(String)
    raw_payload = Column(JSON)
    investigation_summary = Column(Text)
    remediation_log = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SystemEvent(Base):
    """Dead-letter storage for unmapped alerts or system errors."""
    __tablename__ = "system_events"
    id = Column(Integer, primary_key=True)
    event_type = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))