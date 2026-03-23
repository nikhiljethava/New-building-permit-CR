# Building Permit Compliance Portal - Frontend

This is the React-based frontend for the **Building Permit Compliance Portal**. It provides a user-friendly interface for San Paloma County residents to manage their properties, submit building permit applications, and receive instant AI-powered compliance feedback.

## Features

- **User Dashboard**: Overview of properties and permit applications.
- **Permit Management**: Create and track the status of building permits.
- **PDF Submission**: Easy-to-use upload interface for building plan PDFs.
- **Real-time Analysis Visualization**: View detailed compliance reports, including passed checks and specific violations with suggestions for remediation.
- **Interactive AI Chat**: Ask follow-up questions about specific building code violations directly within the app.
- **Modern UI**: Built with React, TailwindCSS, and Lucide icons for a clean, responsive experience.

## Tech Stack

- **Framework**: [Vite](https://vitejs.dev/) + [React](https://reactjs.org/) + [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [TailwindCSS](https://tailwindcss.com/)
- **State Management**: [Zustand](https://github.com/pmndrs/zustand)
- **Icons**: [Lucide-React](https://lucide.dev/)
- **API Communication**: [Axios](https://axios-http.com/)

## Getting Started

### Prerequisites

- Node.js 18+ installed.
- The API Gateway running (default: `http://localhost:8080`).

### Installation

```bash
make install
```

### Running Locally

```bash
make start
```

The application will be available at `http://localhost:5173`.

## Deployment

The frontend can be deployed to Google Cloud Run (hosted via a simple Node.js server) using Cloud Build.

```bash
make deploy
```

This will trigger a build and deployment based on the `.cloudbuild/deploy.yaml` configuration.
