from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

class AppConfig(BaseModel):
    enabled: bool = False
    image_name: str = "app-service"
    port: int = 8000

class GitConfig(BaseModel):
    enabled: bool = False
    repo_name: str = ""
    branch: str = "main"

class ValidationResult(BaseModel):
    tool: str
    status: Literal["PASS", "FAIL"]
    stderr: str = ""

class LiveResource(BaseModel):
    address: str
    type: str
    status: str
    last_synced: datetime = Field(default_factory=datetime.now)

class InfraBlueprint(BaseModel):
    project_name: str
    region: str = "us-east-1"
    vpc_cidr: str = "10.0.0.0/16"
    allowed_mgmt_ips: List[str] = []
    app_config: AppConfig = Field(default_factory=AppConfig)
    model_config = ConfigDict(extra="ignore")

class ComputeResource(BaseModel):
    cpu: int = 1
    memory: str = "1GB"
    disk: str = "10GB"
    resource_type: str = "general"

class IncidentContext(BaseModel):
    id: str
    resource_ip: str
    alert_name: str
    severity: str
    status: str

class AgentState(BaseModel):
    thread_id: str
    user_idea: str
    image_data: Optional[str] = None
    retrieved_policy: str = ""
    current_blueprint: Optional[InfraBlueprint] = None
    artifacts: Dict[str, str] = {}
    diagram_code: str = ""
    validation_results: List[ValidationResult] = []
    deployment_url: Optional[str] = None
    git_config: GitConfig = Field(default_factory=GitConfig)
    # Phase 5: State tracking
    live_resources: List[LiveResource] = []
    # Phase 9: Incident context
    current_incident: Optional[IncidentContext] = None

# Additional classes for TUI
class AgentTask(BaseModel):
    id: str
    agent: str
    status: str
    runtime: str

class SystemMetrics(BaseModel):
    cpu_history: List[int]
    mem_history: List[float]
    total_cost: float
    active_tasks: List[AgentTask]

class LogEntry(BaseModel):
    timestamp: str
    user: str
    cmd: str
    type: str
    message: Optional[str] = None

class ValidationResponse(BaseModel):
    valid: bool
    errors: List[str]

class InfraState(BaseModel):
    resources: List[dict]

class ForgeConfig(BaseModel):
    provider: str
    region: str
    resources: List[dict]