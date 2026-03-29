# Assessor MCP Server

The **Assessor MCP Server** is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides access to San Paloma County's property and zoning data. It allows AI agents to query land use regulations, parcel details, and setback requirements to assist in building permit compliance analysis.

## Features

- **Model Context Protocol**: Implements the MCP standard using the `FastMCP` framework.
- **Property Data**: Lookup parcel information by APN (Assessor's Parcel Number).
- **Zoning Information**: Retrieve zoning classifications for addresses and detailed rules for specific zones.
- **Administrative Tools**: Tools to add parcels, update zoning, and manage zoning rules.
- **SSE Transport**: Exposes the MCP server over Server-Sent Events (SSE) for easy integration.

## Tech Stack

- **Language**: Python 3.12+
- **Framework**: [FastMCP](https://github.com/jlowin/fastmcp)
- **Database**: SQLite

## Exposed Tools

- `lookup_parcel(apn)`: Get property details.
- `get_zoning_classification(address)`: Find the zoning code for an address.
- `get_setback_requirements(zoning_code)`: Get detailed rules (height, coverage, setbacks) for a zone.
- `add_parcel(...)`: Insert a new property record.
- `rezone_address(...)`: Update zoning for an address.
- `add_zoning_rule(...)`: Manage zoning regulations.

## Getting Started

### Prerequisites

- Python 3.12+ installed.
- `uv` package manager (recommended).

### Installation

```bash
make install
```

### Running Locally

```bash
make start
```

The server will start on port `8002` by default and expose the MCP SSE endpoint.

## Onboarding to Agent Registry

Once deployed to Cloud Run, you can register this component with the Agent Registry using the provided script in the `infra` directory:

```bash
cd ../infra
make onboard-assessor
```

## Database

The server uses a local SQLite database (`assessor.db`). On the first run, it will automatically initialize the schema and seed it with sample data for San Paloma County.
