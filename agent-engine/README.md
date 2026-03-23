# Agent Engine Shared Services

This directory contains the deployment logic for the **Vertex AI Reasoning Engine** (also known as Agent Engine) that serves as the shared infrastructure for the Building Permit Compliance Portal.

## Purpose

Instead of deploying individual standalone agents, this component deploys a specialized container to Vertex AI that enables **all agents** in this project to leverage centralized, high-performance services:

- **Vertex AI Session Management:** Provides persistent, scalable conversation session storage across the entire microservice ecosystem.
- **Vertex AI Memorybank:** Enables a long-term "Memory Bank" service that allows agents to retrieve and reference past interactions, violations, and decisions.
- **Unified Tool Specs:** Acts as the registry for method specifications and schemas used by the reasoning engine to orchestrate agent-to-tool and agent-to-agent interactions.

By centralizing these services in the `agent-engine`, we ensure that the **Compliance Agent**, **Contractor Agent**, and **API Gateway** all share a consistent view of the user's history and regulatory context.

## Tech Stack
- **Language:** Python
- **SDK:** `vertexai` (Google Cloud Vertex AI SDK)
- **Framework:** Google ADK (Agent Development Kit)

## Usage

The `agent-engine` is deployed once as part of the infrastructure setup to provide the `REASONING_ENGINE_APP_NAME` required by the other microservices.

### Prerequisites
- Python 3.10+
- `uv` installed.
- Google Cloud project with Vertex AI API enabled.

### Deployment
To deploy or update the shared Reasoning Engine:
```bash
make deploy
```

This runs the deployment utility which:
1.  Packages the shared ADK application logic.
2.  Uploads the source to Vertex AI.
3.  Configures the Reasoning Engine resource with appropriate CPU, memory, and scaling policies.
4.  Outputs the **Reasoning Engine ID**, which should be configured in the `.env` files of the other agents.
