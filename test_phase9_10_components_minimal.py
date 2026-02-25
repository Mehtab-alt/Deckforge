"""
Test script to verify all Phase 9-10 components work together (without database)
"""
from core.schema import ComputeResource, IncidentContext, AgentState
from core.compiler import ProviderFactory
from agents.sre_investigator import SAFE_COMMANDS
from core.models import IncidentStatus
from datetime import datetime
import enum


def test_compute_resource_schema():
    """Test the ComputeResource schema."""
    print("Testing ComputeResource schema...")
    
    resource = ComputeResource(cpu=4, memory="8GB", disk="100GB", resource_type="compute")
    
    assert resource.cpu == 4
    assert resource.memory == "8GB"
    assert resource.disk == "100GB"
    assert resource.resource_type == "compute"
    
    print("✅ ComputeResource schema test passed")


def test_provider_factory_with_compute_resource():
    """Test the ProviderFactory with ComputeResource."""
    print("\nTesting ProviderFactory with ComputeResource...")
    
    factory = ProviderFactory()
    resource_small = ComputeResource(cpu=1, memory="2GB", disk="20GB", resource_type="app_server")
    resource_large = ComputeResource(cpu=8, memory="16GB", disk="200GB", resource_type="app_server")
    
    aws_small = factory.get_sku("aws", resource_small)
    aws_large = factory.get_sku("aws", resource_large)
    
    assert aws_small == "t3.medium"
    assert aws_large == "m5.large"
    
    print(f"✅ AWS mappings: Small={aws_small}, Large={aws_large}")


def test_incident_status_enum():
    """Test the IncidentStatus enum."""
    print("\nTesting IncidentStatus enum...")
    
    assert IncidentStatus.TRIGGERED == "triggered"
    assert IncidentStatus.RESOLVED == "resolved"
    assert IncidentStatus.FAILED == "failed"
    
    all_statuses = [status.value for status in IncidentStatus]
    expected = ["triggered", "investigating", "awaiting_approval", "executing", "resolved", "failed", "unmapped"]
    
    assert all(status in all_statuses for status in expected)
    
    print(f"✅ All incident statuses: {all_statuses}")


def test_sre_investigator_commands():
    """Test the SRE Investigator safe commands."""
    print("\nTesting SRE Investigator safe commands...")
    
    expected_commands = ["df -h", "top -bn1 | head -n 20", "tail -n 50 /var/log/syslog", "uptime"]
    
    assert len(SAFE_COMMANDS) == 4
    for cmd in expected_commands:
        assert cmd in SAFE_COMMANDS
    
    print(f"✅ Safe commands: {SAFE_COMMANDS}")


def test_incident_context():
    """Test the IncidentContext schema."""
    print("\nTesting IncidentContext schema...")
    
    incident_ctx = IncidentContext(
        id="incident-test-123",
        resource_ip="10.0.1.100",
        alert_name="HighCPUUsage",
        severity="critical",
        status="triggered"
    )
    
    assert incident_ctx.id == "incident-test-123"
    assert incident_ctx.resource_ip == "10.0.1.100"
    assert incident_ctx.alert_name == "HighCPUUsage"
    assert incident_ctx.severity == "critical"
    assert incident_ctx.status == "triggered"
    
    print("✅ IncidentContext schema test passed")


def test_agent_state_with_incident():
    """Test AgentState with incident context."""
    print("\nTesting AgentState with incident context...")
    
    agent_state = AgentState(
        thread_id="test-thread-1",
        user_idea="Test incident response",
        current_incident=IncidentContext(
            id="incident-test-456",
            resource_ip="10.0.1.101",
            alert_name="HighMemoryUsage",
            severity="warning",
            status="investigating"
        )
    )
    
    assert agent_state.thread_id == "test-thread-1"
    assert agent_state.current_incident is not None
    assert agent_state.current_incident.id == "incident-test-456"
    assert agent_state.current_incident.alert_name == "HighMemoryUsage"
    
    print("✅ AgentState with incident context test passed")


def run_all_tests():
    """Run all tests."""
    print("Running Phase 9-10 Component Tests...\n")
    
    test_compute_resource_schema()
    test_provider_factory_with_compute_resource()
    test_incident_status_enum()
    test_sre_investigator_commands()
    test_incident_context()
    test_agent_state_with_incident()
    
    print("\n🎉 All Phase 9-10 component tests passed!")
    print("\nImplemented components:")
    print("- Extended database models with Incident, RemediationPolicy, and SystemEvent")
    print("- Incident gateway API for alert ingestion")
    print("- SRE Investigator with safe SSH diagnostics")
    print("- Ansible runbook engine for remediation")
    print("- Multi-cloud Provider Factory with ComputeResource schema")
    print("- Secure Slack ChatOps integration with HMAC verification")
    print("- Proper incident lifecycle management")


if __name__ == "__main__":
    run_all_tests()