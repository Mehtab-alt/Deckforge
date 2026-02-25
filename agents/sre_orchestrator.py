from langgraph.graph import StateGraph, END
from core.schema import AgentState
from agents.sre_investigator import investigate_node
from core.llm_factory import get_llm
from core.memory import memory
import json

def dispatcher_node(state):
    """
    The dispatcher analyzes the investigation summary and decides on remediation actions.
    It selects the appropriate runbook based on the situation report.
    """
    llm = get_llm(json_mode=True)
    
    analysis = state.get('analysis_summary', '')
    situation_report = state.get('situation_report', {})
    
    # Determine the appropriate remediation based on diagnostics
    if 'disk' in analysis.lower() or 'df -h' in situation_report:
        # Check if disk space is low
        df_output = situation_report.get('df -h', '')
        if '95%' in df_output or '96%' in df_output or '97%' in df_output or '98%' in df_output or '99%' in df_output or '100%' in df_output:
            # High disk usage detected, recommend cleanup
            return {
                "selected_runbook": "cleanup_disk",
                "runbook_params": {"target_directory": "/tmp", "dry_run": False},
                "recommended_action": "Clean up temporary files"
            }
        elif 'out of memory' in analysis.lower() or 'memory' in analysis.lower():
            # Memory issue detected, recommend service restart
            return {
                "selected_runbook": "restart_service",
                "runbook_params": {"service_name": "app-service"},
                "recommended_action": "Restart application service"
            }
    
    # Default to restart service if no specific issue is detected
    return {
        "selected_runbook": "restart_service",
        "runbook_params": {"service_name": "app-service"},
        "recommended_action": "Restart application service as general remediation"
    }


def approval_gate_node(state):
    """
    Determines if the remediation action requires human approval based on policy.
    In a real system, this would check the RemediationPolicy table.
    """
    # For now, we'll implement a simple policy check
    selected_runbook = state.get('selected_runbook', '')
    
    # Some actions might require approval
    requires_approval = selected_runbook in ['restart_service', 'cleanup_disk']
    
    if requires_approval:
        # In a real system, this would send a message to Slack
        return {"approval_status": "pending_slack_approval", "next_action": "wait_for_approval"}
    else:
        return {"approval_status": "auto_approved", "next_action": "execute_now"}


def execution_planner_node(state):
    """
    Plans the execution of the remediation task based on approval status.
    """
    approval_status = state.get('approval_status', 'pending')
    
    if approval_status == 'auto_approved':
        # Execute immediately
        return {"execution_status": "ready_to_execute"}
    elif approval_status == 'pending_slack_approval':
        # Wait for Slack approval
        return {"execution_status": "waiting_for_approval"}
    else:
        return {"execution_status": "on_hold"}


# Define the SRE workflow graph
def create_sre_workflow():
    workflow = StateGraph(AgentState)
    
    # Add nodes to the workflow
    workflow.add_node("investigate", investigate_node)
    workflow.add_node("dispatch", dispatcher_node)
    workflow.add_node("approval_gate", approval_gate_node)
    workflow.add_node("execution_planner", execution_planner_node)
    
    # Set entry point
    workflow.set_entry_point("investigate")
    
    # Define edges
    workflow.add_edge("investigate", "dispatch")
    workflow.add_edge("dispatch", "approval_gate")
    workflow.add_edge("approval_gate", "execution_planner")
    
    # For simplicity, ending after planning - in reality, you'd continue to execution
    workflow.add_edge("execution_planner", END)
    
    return workflow.compile()


# The SRE brain
sre_brain = create_sre_workflow()