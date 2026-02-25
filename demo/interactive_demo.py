"""
DeckForge Phases 9-10 Interactive Demo
Autonomous SRE & Multi-Cloud Federation

This program provides an interactive simulation where users can input their own
scenarios and see how the DeckForge system would respond.
"""

import time
import random
import threading
from datetime import datetime
import sys

class Color:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_colored(text, color):
    """Print colored text to terminal"""
    print(f"{color}{text}{Color.ENDC}")

def simulate_loading(message, duration=2):
    """Simulate a loading process with dots"""
    print(f"{message}", end="")
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(" Done!")

def get_user_scenario():
    """Get scenario input from user"""
    print_colored("\n📋 ENTER YOUR SCENARIO", Color.YELLOW)
    print("-" * 40)
    
    print("Enter details for your infrastructure scenario:")
    
    server_name = input("Server name (e.g., web-server-01): ").strip()
    if not server_name:
        server_name = "web-server-01"
    
    issue_type = input("Issue type (e.g., HighCPUUsage, DiskSpaceLow, ServiceDown): ").strip()
    if not issue_type:
        issue_type = "HighCPUUsage"
    
    severity = input("Severity (warning/critical/info) [default: critical]: ").strip()
    if not severity:
        severity = "critical"
    
    project_name = input("Project name (e.g., ecommerce-app): ").strip()
    if not project_name:
        project_name = "my-app"
    
    print(f"\nYour scenario: {issue_type} on {server_name} ({project_name}) - {severity}")
    
    return {
        "name": issue_type,
        "severity": severity,
        "instance": server_name,
        "project": project_name
    }

def show_header():
    """Display the header for the demo"""
    print_colored("="*70, Color.CYAN)
    print_colored("           DECKFORGE PHASES 9-10 INTERACTIVE DEMONSTRATION", Color.BOLD)
    print_colored("         Autonomous SRE & Multi-Cloud Federation", Color.CYAN)
    print_colored("="*70, Color.CYAN)
    print()
    print("This demo simulates the DeckForge platform's autonomous SRE capabilities.")
    print("You can input your own infrastructure scenarios to see how the system responds.")

def show_how_it_works():
    """Explain how the system works"""
    print_colored(f"\n⚙️  HOW DECKFORGE WORKS", Color.BOLD)
    print("=" * 50)
    
    print_colored("\n1. MONITORING INTEGRATION", Color.YELLOW)
    print("   • Integrates with Prometheus, Datadog, New Relic, etc.")
    print("   • Receives alerts via webhook at /hooks/alert")
    print("   • Validates alert authenticity and project mapping")
    
    print_colored("\n2. INCIDENT MANAGEMENT", Color.YELLOW)
    print("   • Creates incident records in database")
    print("   • Tracks lifecycle: TRIGGERED → INVESTIGATING → AWAITING_APPROVAL → EXECUTING → RESOLVED")
    print("   • Stores raw alert payload for analysis")
    
    print_colored("\n3. AUTONOMOUS INVESTIGATION", Color.YELLOW)
    print("   • Runs safe diagnostic commands via SSH")
    print("   • Commands: df -h, top, log analysis, uptime")
    print("   • Security: Keys from env vars, not disk")
    
    print_colored("\n4. AI DECISION ENGINE", Color.YELLOW)
    print("   • Analyzes diagnostic data")
    print("   • Matches patterns to known issues")
    print("   • Recommends appropriate remediation")
    
    print_colored("\n5. SECURITY & APPROVAL", Color.YELLOW)
    print("   • Policy engine determines approval needs")
    print("   • Secure Slack integration with HMAC verification")
    print("   • Human-in-the-loop for critical actions")
    
    print_colored("\n6. AUTOMATED REMEDIATION", Color.YELLOW)
    print("   • Executes Ansible runbooks via ansible-runner")
    print("   • Process isolation and detailed logging")
    print("   • Idempotent operations")
    
    print_colored("\n7. MULTI-CLOUD ABSTRACTION", Color.YELLOW)
    print("   • Maps generic intents to cloud-specific SKUs")
    print("   • Supports AWS, Azure, GCP with lookup tables")
    print("   • Ensures infrastructure portability")

def show_configuration_options():
    """Show configuration options"""
    print_colored(f"\n🔧 CONFIGURATION OPTIONS", Color.BOLD)
    print("=" * 50)
    
    print_colored("\nDATABASE MODELS", Color.GREEN)
    print("   • Incident: Tracks incidents with status, severity, etc.")
    print("   • RemediationPolicy: Defines allowed actions per org/alert")
    print("   • SystemEvent: Dead-letter queue for unmapped alerts")
    
    print_colored("\nPOLICY CONFIGURATION", Color.GREEN)
    print("   • requires_approval: Toggle for human approval")
    print("   • allowed_actions: Whitelist of permitted remediations")
    print("   • max_cost_impact: Budget limits for auto-actions")
    
    print_colored("\nSECURITY SETTINGS", Color.GREEN)
    print("   • SLACK_SIGNING_SECRET: For webhook verification")
    print("   • SRE_SSH_PRIVATE_KEY: For secure connections")
    print("   • DATABASE_URL: Connection string")
    
    print_colored("\nRUNBOOK TEMPLATES", Color.GREEN)
    print("   • Located in templates/runbooks/")
    print("   • restart_service.yml.j2: Service restarts")
    print("   • cleanup_disk.yml.j2: Disk cleanup")
    print("   • Custom runbooks possible")

def show_user_workflow():
    """Show the user workflow"""
    print_colored(f"\n👤 USER WORKFLOW", Color.BOLD)
    print("=" * 50)
    
    print_colored("\nFOR SRE/SYSTEM ADMINS:", Color.CYAN)
    print("   1. Configure monitoring to send alerts to DeckForge")
    print("   2. Set up remediation policies per project")
    print("   3. Review and approve critical actions in Slack")
    print("   4. Monitor incident resolution in dashboard")
    
    print_colored("\nFOR DEVELOPERS:", Color.CYAN)
    print("   1. Define infrastructure as code/blueprints")
    print("   2. Tag resources with project_id for routing")
    print("   3. Monitor service health via integrated dashboards")
    print("   4. Receive notifications when issues are resolved")
    
    print_colored("\nFOR PLATFORM ENGINEERS:", Color.CYAN)
    print("   1. Configure multi-cloud provider mappings")
    print("   2. Set up security policies and approvals")
    print("   3. Customize remediation runbooks")
    print("   4. Monitor platform health and usage")

def simulate_monitoring_system(alert):
    """Simulate monitoring system detecting issues"""
    print_colored(f"\n🔍 MONITORING SYSTEM ACTIVITY", Color.YELLOW)
    print("-" * 40)
    
    print(f"Detected: {alert['name']} on {alert['instance']} ({alert['project']}) - {alert['severity']}")
    time.sleep(1)
    
    return [alert]

def simulate_incident_ingestion(alert):
    """Simulate the incident ingestion process"""
    print_colored(f"\n📡 INCIDENT INGESTION GATEWAY", Color.PURPLE)
    print("-" * 40)
    
    print(f"Incoming alert: {alert['name']} from {alert['instance']}")
    simulate_loading("Validating alert authenticity")
    
    # Simulate project mapping
    print(f"Mapping to project: {alert['project']}")
    simulate_loading("Creating incident record")
    
    incident_id = f"INC-{random.randint(1000, 9999)}"
    print_colored(f"[SUCCESS] Incident created: {incident_id}", Color.GREEN)
    
    return incident_id

def simulate_investigation(incident_id, alert):
    """Simulate the SRE investigation process"""
    print_colored(f"\n🔍 AUTONOMOUS INVESTIGATION (Incident: {incident_id})", Color.BLUE)
    print("-" * 40)
    
    print(f"Connecting to target: {alert['instance']}")
    simulate_loading("Establishing secure SSH connection")
    
    print("Running diagnostic commands...")
    diagnostics = {
        "df -h": "Filesystem      Size  Used Avail Use% /dev/sda1   20G   19G  1.0G  95% /",
        "top -bn1 | head -n 5": "PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND\n 1234 app-user  20   0 2800000 1.8gb  15000 S  98.0 23.5   1234:56 app-server",
        "uptime": " 10:30:15 up 42 days,  5:22,  1 user,  load average: 2.45, 1.87, 1.56"
    }
    
    for cmd, result in diagnostics.items():
        print_colored(f"  $ {cmd}", Color.CYAN)
        print(f"    {result[:60]}...")
        time.sleep(0.5)
    
    print_colored("\n[SUCCESS] Investigation complete", Color.GREEN)
    return diagnostics

def simulate_decision_making(diagnostics, alert):
    """Simulate the decision-making process"""
    print_colored(f"\n🧠 AI DECISION ENGINE", Color.YELLOW)
    print("-" * 40)
    
    print("Analyzing diagnostic data...")
    time.sleep(1)
    
    # Analyze the diagnostics based on the alert type
    if "DiskSpaceLow" in alert['name'] or "95%" in diagnostics["df -h"]:
        issue_desc = "Critical disk space issue detected (95% usage)"
        recommended_action = "cleanup_disk"
        print_colored(f"  • {issue_desc}", Color.RED)
    elif "HighCPU" in alert['name'] or "98.0" in diagnostics["top -bn1 | head -n 5"]:
        issue_desc = "High CPU usage detected"
        recommended_action = "restart_service"
        print_colored(f"  • {issue_desc}", Color.RED)
    else:
        issue_desc = "Service may be unresponsive"
        recommended_action = "restart_service"
        print_colored(f"  • {issue_desc}", Color.RED)
    
    print("\nRecommended actions:")
    if recommended_action == "cleanup_disk":
        print_colored("  1. Clean up temporary files", Color.YELLOW)
        print_colored("  2. Check for log accumulation", Color.YELLOW)
    else:
        print_colored("  1. Restart problematic service", Color.YELLOW)
        print_colored("  2. Check application logs", Color.YELLOW)
    
    # Determine if approval is needed based on severity
    requires_approval = alert['severity'] == 'critical'
    print(f"\nPolicy check: Approval {'REQUIRED' if requires_approval else 'NOT REQUIRED'} for {alert['severity']} severity")
    
    return recommended_action, requires_approval

def simulate_slack_notification(incident_id, recommended_action, requires_approval):
    """Simulate sending notification to Slack"""
    if not requires_approval:
        print_colored(f"\n✅ AUTO-APPROVED (low severity)", Color.GREEN)
        print("-" * 40)
        print("Action automatically approved based on policy.")
        return True
    
    print_colored(f"\n💬 SLACK CHATOPS INTEGRATION", Color.PURPLE)
    print("-" * 40)
    
    print("Sending remediation request to Slack...")
    print_colored(f"  Channel: #infrastructure-alerts", Color.CYAN)
    print(f"  Message: Incident {incident_id} - {recommended_action}")
    print("  Actions: [Approve] [Reject] [Escalate]")
    
    simulate_loading("Waiting for human approval")
    
    # Simulate human approval after delay
    time.sleep(2)
    print_colored("  [APPROVED] Approval received from @sre-team-lead", Color.GREEN)
    
    return True  # Approved

def simulate_remediation(incident_id, action, approved):
    """Simulate the remediation process"""
    if not approved:
        print_colored(f"\n❌ REMEDIATION CANCELLED", Color.RED)
        print("-" * 40)
        print("Action was not approved. Incident remains open for manual handling.")
        return False
    
    print_colored(f"\n🔧 EXECUTING REMEDIATION (Incident: {incident_id})", Color.GREEN)
    print("-" * 40)
    
    print(f"Running Ansible playbook: {action}.yml")
    simulate_loading("Executing remediation steps")
    
    # Simulate remediation steps based on action
    if action == "cleanup_disk":
        steps = [
            "Identifying large temporary files",
            "Removing old log files",
            "Clearing cache directories",
            "Verifying disk space freed",
            "Monitoring for stability"
        ]
    else:  # restart_service
        steps = [
            "Checking service status",
            "Stopping service gracefully",
            "Starting service",
            "Verifying service health",
            "Monitoring for stability"
        ]
    
    for step in steps:
        print(f"  [STEP] {step}")
        time.sleep(0.7)
    
    print_colored("\n[SUCCESS] Remediation completed successfully!", Color.GREEN)
    return True

def simulate_multi_cloud_abstraction():
    """Simulate multi-cloud resource mapping"""
    print_colored(f"\n☁️  MULTI-CLOUD FEDERATION", Color.CYAN)
    print("-" * 40)
    
    print("Mapping infrastructure intent to cloud-specific resources...")
    
    # Simulate resource requirements
    resource_req = {
        "cpu": random.choice([2, 4, 8]),
        "memory": random.choice(["4GB", "8GB", "16GB"]),
        "disk": random.choice(["50GB", "100GB", "200GB"]),
        "type": "application_server"
    }
    
    print(f"Required: {resource_req['cpu']} CPU, {resource_req['memory']} RAM, {resource_req['disk']} Disk")
    
    # Map to different clouds
    cloud_mappings = {
        "AWS": "m5.large" if resource_req['cpu'] <= 4 else "m5.xlarge",
        "Azure": "Standard_B2s" if resource_req['cpu'] <= 4 else "Standard_D2_v3",
        "GCP": "e2-medium" if resource_req['cpu'] <= 4 else "e2-standard-2"
    }
    
    for cloud, sku in cloud_mappings.items():
        print(f"  {cloud}: {sku}")
        time.sleep(0.5)
    
    print_colored("\n[SUCCESS] Cloud abstraction layer ensures portability", Color.GREEN)

def simulate_resolution(incident_id, remediated):
    """Simulate incident resolution"""
    print_colored(f"\n✅ INCIDENT RESOLUTION", Color.GREEN)
    print("-" * 40)
    
    if remediated:
        print(f"Incident {incident_id} status: RESOLVED")
        print("Resolution: Automatic remediation successful")
        print("Verification: Service health confirmed")
    else:
        print(f"Incident {incident_id} status: AWAITING_MANUAL_RESOLUTION")
        print("Resolution: Action cancelled, requires manual intervention")
    
    print(f"Time to resolution: {random.randint(3, 8)} minutes")
    print_colored("\n[SUCCESS] Incident lifecycle complete", Color.GREEN)

def show_dashboard_summary():
    """Show a summary dashboard"""
    print_colored(f"\n📊 SYSTEM DASHBOARD SUMMARY", Color.BOLD)
    print("=" * 50)
    
    stats = [
        ("Incidents Handled", random.randint(20, 30)),
        ("Avg. Resolution Time", f"{round(random.uniform(4.0, 6.5), 1)} min"),
        ("Success Rate", f"{random.randint(95, 99)}%"),
        ("Manual Interventions", random.randint(1, 5)),
        ("Cost Savings", f"${random.randint(10000, 15000)}")
    ]
    
    for stat, value in stats:
        print(f"{stat:<20}: {value}")
    
    print_colored("\n[ROCKET] DeckForge Autonomous SRE Active", Color.GREEN)
    print("   • Continuous monitoring")
    print("   • Automated investigation") 
    print("   • Intelligent remediation")
    print("   • Multi-cloud federation")

def run_interactive_demo():
    """Run the complete interactive demo"""
    show_header()
    
    while True:
        print_colored(f"\n[GAMEPAD] SELECT DEMO MODE", Color.BOLD)
        print("1. Enter your own scenario")
        print("2. Learn how DeckForge works")
        print("3. View configuration options")
        print("4. Understand user workflow")
        print("5. Run demo with sample scenario")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            # Get user scenario
            alert = get_user_scenario()
            
            print_colored(f"\n🚀 RUNNING DEMO FOR YOUR SCENARIO", Color.BOLD)
            print("=" * 50)
            print(f"Simulating: {alert['name']} on {alert['instance']} ({alert['project']})")
            
            # Run the complete workflow
            incident_id = simulate_incident_ingestion(alert)
            diagnostics = simulate_investigation(incident_id, alert)
            action, requires_approval = simulate_decision_making(diagnostics, alert)
            approved = simulate_slack_notification(incident_id, action, requires_approval)
            remediated = simulate_remediation(incident_id, action, approved)
            simulate_multi_cloud_abstraction()
            simulate_resolution(incident_id, remediated)
            show_dashboard_summary()
            
        elif choice == "2":
            show_how_it_works()
            
        elif choice == "3":
            show_configuration_options()
            
        elif choice == "4":
            show_user_workflow()
            
        elif choice == "5":
            # Sample scenario
            sample_alert = {
                "name": "DiskSpaceLow", 
                "severity": "critical", 
                "instance": "db-server-01", 
                "project": "customer-db"
            }
            print_colored(f"\n🚀 RUNNING DEMO WITH SAMPLE SCENARIO", Color.BOLD)
            print("=" * 50)
            print(f"Simulating: {sample_alert['name']} on {sample_alert['instance']} ({sample_alert['project']})")
            
            # Run the complete workflow
            incident_id = simulate_incident_ingestion(sample_alert)
            diagnostics = simulate_investigation(incident_id, sample_alert)
            action, requires_approval = simulate_decision_making(diagnostics, sample_alert)
            approved = simulate_slack_notification(incident_id, action, requires_approval)
            remediated = simulate_remediation(incident_id, action, approved)
            simulate_multi_cloud_abstraction()
            simulate_resolution(incident_id, remediated)
            show_dashboard_summary()
            
        elif choice == "6":
            print_colored("\n👋 THANK YOU FOR USING DECKFORGE DEMO!", Color.GREEN)
            print("DeckForge transforms infrastructure management with autonomous SRE capabilities.")
            break
            
        else:
            print("Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    try:
        run_interactive_demo()
    except KeyboardInterrupt:
        print_colored("\n\nDemo interrupted by user.", Color.RED)
        sys.exit(0)