# Contractor Agent

This directory contains the Python-based AI agent that simulates a building contractor. It interacts with the main compliance agent (and end-users) to discuss building plans, clarify violations, and propose structural remediation based on regulatory feedback.

## Setup & Local Development

### Prerequisites
- Python 3.12+
- `uv` (for fast Python package management)

### Installation

To install dependencies using `uv`, run the following command from this directory:

```bash
uv sync
```

### Starting the Server

The contractor agent is built with FastAPI and conforms to the Agent-to-Agent (A2A) protocol. You can start the local development server using the provided `Makefile`:

```bash
make start
```

This will run `uvicorn main:app --reload --port 8001`, making the agent accessible at `http://127.0.0.1:8001`.

## Onboarding to Agent Registry

After deployment to Google Cloud Run, register this agent via its `.well-known/agent-card.json`:

```bash
cd ../infra
make onboard-contractor
```

## Integration

The main API gateway (written in Go) expects this agent to be running and proxies requests to it. Make sure both the main `agent` and this `contractor-agent` are running simultaneously when testing the full system locally.
