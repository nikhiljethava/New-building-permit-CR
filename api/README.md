# Building Permit API Gateway

This is the Go-based API Gateway for the **Building Permit Compliance Portal**. It handles user authentication, property and permit management, and acts as a bridge between the frontend and the AI-powered Compliance and Contractor agents.

## Features

- **User & Property Management**: Simple email-based login and CRUD operations for properties and permits.
- **Compliance Analysis Proxy**: Handles PDF uploads and forwards them to the Compliance Agent for analysis.
- **Interactive Chat Proxy**: Proxies conversational requests to the Compliance and Contractor agents.
- **Data Persistence**: Stores user data, permit history, and analysis reports in a SQLite database.
- **Observability**: Integrated with OpenTelemetry for distributed tracing on Google Cloud.

## Tech Stack

- **Language**: Go 1.21+
- **Framework**: [Gin Gonic](https://gin-gonic.com/)
- **ORM**: [GORM](https://gorm.io/)
- **Database**: SQLite (via GORM)
- **Tracing**: OpenTelemetry with Google Cloud Trace exporter

## Getting Started

### Prerequisites

- Go installed on your machine.
- Access to the Compliance Agent (default: `http://localhost:8000`).

### Installation

```bash
make install
```

### Running Locally

```bash
make start
```

The server will start on port `8080` by default.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | The port the API will listen on. | `8080` |
| `DB_NAME` | The name of the SQLite database file. | `building_plans.db` |
| `AGENT_URL` | The URL of the Compliance Agent. | `http://127.0.0.1:8000/analyze` |
| `CONTRACTOR_AGENT_URL` | The URL of the Contractor Agent. | `http://127.0.0.1:8001/chat` |
| `GOOGLE_CLOUD_PROJECT` | Required for OpenTelemetry tracing. | (None) |

## API Endpoints

### Authentication & Profiles
- `POST /api/login`: Login or register a user.
- `GET /api/users/:id/properties`: List properties for a user.
- `POST /api/users/:id/properties`: Add a new property.

### Permits
- `GET /api/properties/:id/permits`: List permits for a property.
- `POST /api/properties/:id/permits`: Create a permit application.
- `GET /api/permits/:id`: Get permit details and submission history.
- `DELETE /api/permits/:id`: Delete a permit application.

### AI Integration
- `POST /api/analyze-plan`: Upload a PDF for compliance analysis.
- `POST /api/chat`: Send a follow-up question to the Compliance Agent.
- `POST /api/contractor-chat`: Send a question to the Contractor Agent.

## Deployment

The API is configured for deployment to Google Cloud Run using Cloud Build.

```bash
make deploy
```

Refer to `.cloudbuild/deploy.yaml` for the deployment configuration.
