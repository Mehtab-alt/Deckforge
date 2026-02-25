# DeckForge: AI-Powered Infrastructure Generation Platform

DeckForge is an advanced platform that transforms natural language descriptions and visual diagrams into production-ready infrastructure code. By leveraging AI and automation, it accelerates infrastructure provisioning while ensuring compliance with organizational standards. This version represents a major architectural upgrade to a commercial SaaS platform with distributed components and enhanced scalability features.

## Features

- **Multi-Modal Input**: Accept both text descriptions and visual diagrams as input
- **AI-Powered Generation**: Converts ideas into Terraform, Ansible, Docker, and CI/CD configurations
- **RAG-Based Policy Enforcement**: Integrates corporate standards and security policies
- **Automated Validation**: Validates infrastructure code against best practices
- **Direct GitHub Integration**: Deploys code directly to GitHub repositories
- **State Tracking**: Monitors and tracks live infrastructure resources

## Architecture Overview (Phase 5-8)

```
Architecture (Phases 5-8 - Commercial SaaS):
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User (Web)    │───▶│  Streamlit      │───▶│  FastAPI        │
│                 │    │  Frontend        │    │  Backend        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                                │
┌─────────────────┐    ┌──────────────────┐             ▼
│   Knowledge     │───▶│  LangGraph      │    ┌─────────────────┐
│   Base          │    │  AI Engine       │    │  Celery         │
│(Standards/PDFs) │    │                  │    │  Worker         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                                │
┌─────────────────┐    ┌──────────────────┐             ▼
│  Delivery &     │◀───│  State &        │     ┌─────────────────┐
│  Deployment     │    │  Monitoring      │    │  PostgreSQL     │
│(GitHub, etc.)   │    │  Engine          │    │  Database       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                                 │
┌─────────────────┐    ┌──────────────────┐             ▼
│  RBAC &         │    │  Redis           │    ┌─────────────────┐
│  Authentication │    │  Message Queue   │    │  Export Volume  │
│                 │    │  (Shared)        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Prerequisites

- Python 3.9+
- Terraform installed in your PATH
- An OpenAI API key
- A GitHub personal access token (optional, for GitHub integration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/deckforge.git
cd deckforge
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Add your corporate standards to the `knowledge_base/` directory (Markdown or PDF format)

## Usage (Phase 5-8)

### Running Locally with Docker (Recommended)

```bash
# Build and run all services
docker-compose build
docker-compose up
```

The application will be available at `http://localhost:8501` for the frontend, and API documentation at `http://localhost:8000/docs`.

### Development Notes

For local development, you can also run individual services separately. The new architecture separates concerns into distinct containers for better scalability and maintainability.

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `GITHUB_TOKEN`: GitHub personal access token (for direct repository creation)
- `DEBUG`: Set to `true` to enable debug logging
- `LOG_LEVEL`: Logging level (default: INFO)
- `KNOWLEDGE_BASE_PATH`: Path to knowledge base directory (default: knowledge_base)
- `EXPORTS_PATH`: Path to store generated code (default: exports)

### Knowledge Base

Place your organization's standards, policies, and best practices in the `knowledge_base/` directory in Markdown (.md) or PDF format. DeckForge will use this information to ensure generated infrastructure complies with your organization's requirements.

## Project Structure (Phase 5-8)

```
deckforge/
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── app_frontend.py         # Streamlit UI (Frontend - Thin Client)
├── docker-compose.yml      # Multi-container setup (Phase 7)
├── Dockerfile.api          # API Container (Phase 7)
├── Dockerfile.worker       # Worker Container (Phase 7)
├── knowledge_base/         # Place your MD/PDF standards here (Phase 3)
├── exports/                # Shared volume for generated code (Phase 4)
├── api/                    # Headless Backend (Phase 7)
│   ├── __init__.py
│   ├── main.py             # FastAPI Routes
│   ├── auth.py             # RBAC & Authentication (Phase 6)
│   └── dependencies.py     # API Dependencies
├── core/                   # Core functionality modules (Phase 6/8)
│   ├── __init__.py
│   ├── database.py         # PostgreSQL Connection (Phase 7)
│   ├── models.py           # SQLAlchemy Tables (Phase 6/8)
│   ├── state_parser.py     # Terraform State Parsing (Phase 5)
│   └── marketplace.py      # Module Loader (Phase 8)
└── worker/                 # Async Processing (Phase 7)
    ├── __init__.py
    ├── celery_app.py       # Celery Configuration
    └── tasks.py            # Async Tasks (Phase 1-4 Logic)
```

## Templates (Phase 5-8)

DeckForge comes with expert-crafted templates for:

- **Terraform**: Infrastructure provisioning
- **Ansible**: Security hardening and configuration management
- **Docker**: Containerization
- **CI/CD**: GitHub Actions workflows
- **Documentation**: Auto-generated README files

These templates can be customized to match your organization's specific requirements.

## Deployment (Phase 7-8)

To launch the full Phase 8 stack, run the following commands from the project root directory:

```bash
# Build the containers
docker-compose build

# Run the services
docker-compose up
```

### Access Points

- **Frontend**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Database**: Accessible via port 5432

### Services

- **Frontend**: Streamlit Web UI (Thin Client)
- **API**: FastAPI Backend Service
- **Worker**: Celery Async Worker
- **Database**: PostgreSQL (Production Database)
- **Message Broker**: Redis (Task Queue)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.