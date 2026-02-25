import httpx
import asyncio
from typing import List, Optional, Dict, Any, Type, TypeVar
from pydantic import BaseModel, ValidationError
from core.schema import (
    InfraState, AgentTask, SystemMetrics, 
    LogEntry, ForgeConfig, ValidationResponse
)

T = TypeVar("T", bound=BaseModel)

class APIBridge:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            timeout=10.0
        )
        self.failure_count = 0
        self.degraded_mode = False

    async def _request(self, method: str, endpoint: str, model: Type[T], **kwargs) -> T:
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            if response.status_code >= 500:
                self.failure_count += 1
                if self.failure_count > 3: self.degraded_mode = True
            else:
                self.failure_count = 0
                self.degraded_mode = False
            
            response.raise_for_status()
            return model.model_validate(response.json())
        except Exception as e:
            raise RuntimeError(f"API Error: {str(e)}")

    async def get_metrics(self) -> SystemMetrics:
        return await self._request("GET", "/metrics/summary", SystemMetrics)

    async def get_infra_structure(self) -> Dict:
        response = await self.client.get("/templates/structure")
        return response.json()

    async def validate_template(self, content: str) -> ValidationResponse:
        return await self._request("POST", "/api/validate", ValidationResponse, json={"content": content})

    async def send_agent_hint(self, command: str):
        await self.client.post("/agent/investigator/hint", json={"command": command})

    async def fetch_logs(self) -> List[LogEntry]:
        return await self._request("GET", "/agent/logs", List[LogEntry])