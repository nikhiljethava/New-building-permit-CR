# Building Permit Compliance Agent

This is the Python-based AI agent for the **Building Permit Compliance Portal**. It is responsible for analyzing building plan PDFs, extracting text, querying building codes, and generating compliance reports. It also powers the interactive chat feature for discussing specific violations.

## Features

- **Document Understanding**: Uses Google Cloud Document AI to extract high-fidelity text and layout information from complex PDF architectural drawings.
- **Visual Analysis**: Leverages Gemini 2.5 Pro/Flash to visually inspect building plans alongside the extracted text.
- **RAG Integration**: Queries the California Building Standards Code and San Paloma County reach codes using Vertex AI RAG via a `FunctionTool` to maintain multimodal compatibility.
- **Safety Guardrails**: Implements Model Armor to protect against prompt injection, hate speech, and custom PII filtering (e.g., blocking legal liability phrases).
- **Persistent Context**: Uses the Vertex AI Agent Engine for centralized session management and memory across all agents in the ecosystem.
- **A2A Interoperability**: Integrates with the Contractor Agent using the Agent-to-Agent (A2A) protocol.
- **Assessor Data Integration**: Uses a Model Context Protocol (MCP) server to lookup parcel and zoning data.
- **Observability**: Fully instrumented with OpenTelemetry and Google Cloud Trace.

## Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **AI/ML**: Vertex AI (Gemini), Document AI, Vertex AI RAG Engine
- **Tooling**: Google ADK (Agent Development Kit), `a2a-sdk`

## Getting Started

### Prerequisites

- Python 3.12+ installed.
- `uv` package manager (recommended).
- A Google Cloud Project with Billing enabled.
- Necessary APIs enabled (Vertex AI, Document AI).
- Document AI Processor ID (refer to the main project `README.md` for manual setup instructions).

### Installation

```bash
make install
```

### Environment Variables

You need to set up a `.env` file in this directory. A sample `.env.example` might look like:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
DOCUMENT_AI_PROCESSOR_ID=your-processor-id
DOCUMENT_AI_LOCATION=us
VERTEX_RAG_CORPUS_NAME=projects/your-project/locations/us-central1/ragCorpora/your-corpus-id
GEMINI_MODEL_NAME=gemini-2.5-pro
REASONING_ENGINE_APP_NAME=projects/your-project/locations/us-central1/reasoningEngines/your-engine-id
CONTRACTOR_AGENT_URL=http://0.0.0.0:8001/a2a/building_permit_contractor_agent/.well-known/agent-card.json
ASSESSOR_MCP_SERVER_URL=http://0.0.0.0:8002
```

### Running Locally

```bash
make start
```

The server will start on port `8000` by default.

## API Endpoints

- `POST /analyze`: Core analysis endpoint. Accepts a PDF file and returns a structured JSON compliance report.
- `POST /chat`: Conversational endpoint. Accepts a chat history and context about a violation, and returns a response from the AI agent.
- `GET /health`: Health check endpoint.

## Deployment

The agent can be deployed to Google Cloud Run using Cloud Build.

```bash
make deploy
```
