# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from services import ai_service

from google.adk.cli.fast_api import get_fast_api_app

from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, get_aggregated_resources
from opentelemetry.resourcedetector.gcp_resource_detector import GoogleCloudResourceDetector
import google.auth
import google.auth.transport.requests
# from telemetry import setup_telemetry

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenTelemetry
# setup_telemetry()

allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bucket_name = f"gs://{os.getenv("GOOGLE_CLOUD_PROJECT")}"

# Set OpenTelemetry resource attributes
otel_attrs = os.environ.get("OTEL_RESOURCE_ATTRIBUTES", "")
new_attrs = "functional_type=Agent,cloud.provider=gcp,cloud.account.id=" + os.getenv("GOOGLE_CLOUD_PROJECT", "") + ",gcp.project_id=" + os.getenv("GOOGLE_CLOUD_PROJECT", "")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "")
if location:
    new_attrs += ",cloud.region=" + location

if otel_attrs:
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = otel_attrs + "," + new_attrs
else:
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = new_attrs


app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False,
    artifact_service_uri=bucket_name,
    allow_origins=allow_origins,
    trace_to_cloud=False,
    otel_to_cloud=False,
)

# Manual OTel setup for App Hub
try:
    credentials, project_id = google.auth.default()
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "x-goog-user-project": project_id,
    }
    
    resource = get_aggregated_resources(
        detectors=[GoogleCloudResourceDetector()],
    )
    
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint="https://telemetry.googleapis.com/v1/traces",
                headers=headers,
            )
        )
    )
    trace.set_tracer_provider(tracer_provider)
    print("Telemetry initialized manually successfully.")
except Exception as e:
    print(f"Warning: Failed to initialize Telemetry manually. Error: {e}")

app.title = "Building Plan Compliance Agent"

PROJECT_NUMBER = os.getenv("PROJECT_NUMBER", "271301686744")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

agent_cais = f"//run.googleapis.com/projects/{PROJECT_NUMBER}/locations/{REGION}/services/building-permit-agent"
contractor_cais = f"//run.googleapis.com/projects/{PROJECT_NUMBER}/locations/{REGION}/services/building-permit-contractor-agent"
assessor_cais = f"//run.googleapis.com/projects/{PROJECT_NUMBER}/locations/{REGION}/services/building-permit-assessor-mcp"

def server_request_hook(span, scope):
    span.set_attribute("cloud.provider", "gcp")
    span.set_attribute("cloud.resource.id", agent_cais)
    span.set_attribute("gcp.resource.name", agent_cais)

def client_request_hook(span, request):
    span.set_attribute("cloud.provider", "gcp")
    span.set_attribute("source.cloud.resource.id", agent_cais)
    
    url = str(request.url)
    if "contractor-agent" in url:
        span.set_attribute("gcp.resource.name", contractor_cais)
        span.set_attribute("destination.cloud.resource.id", contractor_cais)
        span.set_attribute("peer.service", "building-permit-contractor-agent")
    elif "assessor-mcp" in url:
        span.set_attribute("gcp.resource.name", assessor_cais)
        span.set_attribute("destination.cloud.resource.id", assessor_cais)
        span.set_attribute("peer.service", "building-permit-assessor-mcp")

HTTPXClientInstrumentor().instrument(request_hook=client_request_hook)
FastAPIInstrumentor.instrument_app(app, server_request_hook=server_request_hook)

class Violation(BaseModel):
    section: str
    description: str
    suggestion: str

class ComplianceReport(BaseModel):
    status: str
    violations: List[Violation]
    approved_elements: List[str]

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    permit_id: Optional[str] = None
    violation: Optional[Violation] = None

class ChatChoice(BaseModel):
    message: ChatMessage

class ChatResponse(BaseModel):
    choices: List[ChatChoice]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response_text = await ai_service.chat_about_violation(request)
        return ChatResponse(
            choices=[
                ChatChoice(
                    message=ChatMessage(
                        role="assistant",
                        content=response_text
                    )
                )
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=ComplianceReport)
async def analyze_plan(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Read the file content asynchronously
    content = await file.read()

    # 1. Use Document AI to extract text (Optional, if we want to query RAG with text specifically)
    extracted_text = ai_service.extract_text_from_pdf(content)
    # log the extracted text
    logger.info(f"Extracted text: {extracted_text}")
    # 2. Use Gemini and Vertex RAG to analyze the plan (passing the raw PDF for Vision)
    analysis_result = await ai_service.analyze_plan_with_gemini(extracted_text, content)

    # Return structured JSON
    return ComplianceReport(**analysis_result)

@app.get("/health")
def health_check():
    return {"status": "ok"}
