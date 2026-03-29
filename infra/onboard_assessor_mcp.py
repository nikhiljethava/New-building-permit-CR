import os
import sys
import json
import subprocess
import urllib.request
from urllib.error import URLError

def get_gcloud_config(prop):
    result = subprocess.run(["gcloud", "config", "get-value", prop], capture_output=True, text=True)
    return result.stdout.strip()

def get_project_number(project_id):
    result = subprocess.run(["gcloud", "projects", "describe", project_id, "--format=value(projectNumber)"], capture_output=True, text=True)
    return result.stdout.strip()

def get_cloud_run_url(service_name, region):
    result = subprocess.run(["gcloud", "run", "services", "describe", service_name, "--region", region, "--format=value(status.url)"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def main():
    project_id = os.environ.get("PROJECT_ID") or get_gcloud_config("project")
    if not project_id:
        print("Error: Could not determine PROJECT_ID.")
        sys.exit(1)
        
    project_number = get_project_number(project_id)
    region = os.environ.get("REGION", "us-central1")
    service_name = "building-permit-assessor-mcp"
    agent_name = "assessor-mcp-server"
    
    print(f"Using Project ID: {project_id}")
    print(f"Using Project Number: {project_number}")
    print(f"Using Region: {region}")
    
    print(f"Retrieving Cloud Run URL for '{service_name}'...")
    service_url = get_cloud_run_url(service_name, region)
    if not service_url:
        print(f"Error: Failed to fetch the URL for service {service_name}")
        sys.exit(1)
        
    mcp_url = f"{service_url}/mcp"
    print(f"MCP URL is: {mcp_url}")
    
    print("Initializing MCP Session to fetch Session ID...")
    init_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "clientInfo": {
                "name": "onboarding-script",
                "version": "1.0.0"
            }
        }
    }
    
    req = urllib.request.Request(mcp_url, data=json.dumps(init_data).encode("utf-8"))
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    
    try:
        with urllib.request.urlopen(req) as response:
            session_id = response.getheader("Mcp-Session-Id")
            if not session_id:
                print("Error: Failed to obtain MCP Session ID from headers.")
                sys.exit(1)
            print(f"Received Session ID: {session_id}")
    except URLError as e:
        print(f"Error during initialization request: {e}")
        sys.exit(1)
        
    print("Fetching tools listing from MCP Server...")
    tools_data = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    req2 = urllib.request.Request(mcp_url, data=json.dumps(tools_data).encode("utf-8"))
    req2.add_header("Content-Type", "application/json")
    req2.add_header("Accept", "application/json,text/event-stream")
    req2.add_header("Mcp-Session-Id", session_id)
    
    try:
        with urllib.request.urlopen(req2) as response:
            tools_resp = json.loads(response.read().decode("utf-8"))
            spec_content = json.dumps(tools_resp.get("result", {}))
    except URLError as e:
        print(f"Error fetching tools list: {e}")
        sys.exit(1)
        
    with open("assessor-mcp-spec.json", "w") as f:
        json.dump(tools_resp, f, indent=2)
    print("Saved spec to assessor-mcp-spec.json")
    
    print(f"Checking if Agent Registry service '{agent_name}' exists in region {region}...")
    check_result = subprocess.run([
        "gcloud", "alpha", "agent-registry", "services", "describe",
        agent_name, "--location", region, "--project", project_id
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if check_result.returncode == 0:
        print(f"Agent '{agent_name}' already exists in region {region}. Skipping creation.")
    else:
        print(f"Agent '{agent_name}' not found. Creating...")
        create_args = [
            "gcloud", "alpha", "agent-registry", "services", "create", agent_name,
            f"--project={project_id}",
            f"--display-name={agent_name}",
            "--description=Assessor MCP Server",
            f"--location={region}",
            "--mcp-server-spec-type=tool-spec",
            f"--mcp-server-spec-content={spec_content}",
            f'--interfaces=[{{"protocolBinding": "jsonrpc", "url": "{mcp_url}"}}]'
        ]
        
        create_result = subprocess.run(create_args)
        if create_result.returncode == 0:
            print(f"Successfully created agent '{agent_name}'.")
        else:
            print(f"Failed to create agent '{agent_name}'.")
            sys.exit(1)

if __name__ == "__main__":
    main()
