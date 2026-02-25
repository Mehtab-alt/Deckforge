# DeckForge Interactive Demo Instructions

## How to Run the Interactive Demo

To run the interactive demo, open a command prompt and execute:

```
python demo/interactive_demo.py
```

## Demo Options

The interactive demo provides the following options:

### 1. Enter Your Own Scenario
- Input custom server names, issue types, severities, and project names
- See how DeckForge would respond to your specific infrastructure scenario
- Experience the complete workflow from alert to resolution

### 2. Learn How DeckForge Works
- Detailed explanation of each component:
  - Monitoring Integration
  - Incident Management
  - Autonomous Investigation
  - AI Decision Engine
  - Security & Approval Process
  - Automated Remediation
  - Multi-Cloud Abstraction

### 3. View Configuration Options
- Database models and their purposes
- Policy configuration settings
- Security settings and secrets
- Runbook templates and customization

### 4. Understand User Workflow
- For SRE/System Admins
- For Developers
- For Platform Engineers

### 5. Run Demo with Sample Scenario
- Experience the complete workflow with a pre-defined scenario
- See all the steps in action without entering custom data

## Real System Configuration

In a real DeckForge deployment, you would configure:

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SLACK_SIGNING_SECRET`: For verifying Slack webhooks
- `SRE_SSH_PRIVATE_KEY`: For secure SSH connections
- `REDIS_URL`: For Celery task queue

### Monitoring Integration
- Configure your monitoring system (Prometheus, Datadog, etc.) to send alerts to:
  `POST /hooks/alert`
- Alerts should include a `project_id` label for proper routing

### Policy Configuration
- Define remediation policies in the database
- Specify which actions require human approval
- Set cost impact limits for automated actions

### Runbook Templates
- Customize Ansible playbooks in `templates/runbooks/`
- Add new remediation procedures as needed
- Test runbooks in isolated environments first

## User Workflow

### For SREs/System Administrators:
1. Configure monitoring to send alerts to DeckForge
2. Set up remediation policies per project
3. Review and approve critical actions in Slack
4. Monitor incident resolution in dashboard

### For Developers:
1. Define infrastructure as code/blueprints
2. Tag resources with project_id for routing
3. Monitor service health via integrated dashboards
4. Receive notifications when issues are resolved

### For Platform Engineers:
1. Configure multi-cloud provider mappings
2. Set up security policies and approvals
3. Customize remediation runbooks
4. Monitor platform health and usage

## Key Benefits

- **Automation**: Reduces manual intervention for routine issues
- **Security**: Multiple approval layers for critical actions
- **Scalability**: Handles multiple incidents simultaneously
- **Portability**: Works across multiple cloud providers
- **Compliance**: Full audit trail of all actions
- **Reliability**: Thorough validation before executing changes