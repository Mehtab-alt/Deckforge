import os
import paramiko
from typing import Dict, Any
from core.schema import AgentState

SAFE_COMMANDS = [
    "df -h", "top -bn1 | head -n 20", "tail -n 50 /var/log/syslog", "uptime"
]

class SREInvestigator:
    def __init__(self, host: str):
        self.host = host
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def _get_private_key(self):
        """Harden security: Fetch key from environment/vault instead of disk."""
        key_data = os.getenv("SRE_SSH_PRIVATE_KEY")
        if not key_data: raise Exception("SSH Key missing in environment")
        return paramiko.RSAKey.from_private_key_file(key_data)

    def run_diagnostics(self) -> Dict[str, str]:
        results = {}
        self.client.connect(hostname=self.host, username="deckforge-sre", pkey=self._get_private_key())
        for cmd in SAFE_COMMANDS:
            _, stdout, _ = self.client.exec_command(cmd)
            results[cmd] = stdout.read().decode()
        self.client.close()
        return results

def investigate_node(state: AgentState):
    investigator = SREInvestigator(state.current_incident.resource_ip)
    telemetry = investigator.run_diagnostics()
    
    # Analysis Summary field for the Dispatcher
    analysis = f"Disk Usage: {telemetry['df -h']}\nRecent Logs: {telemetry['tail -n 50 /var/log/syslog']}"
    return {
        "situation_report": telemetry,
        "analysis_summary": analysis,
        "history": state.history + ["Investigator: Diagnostics gathered."]
    }