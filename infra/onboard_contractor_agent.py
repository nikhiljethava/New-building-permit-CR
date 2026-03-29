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
    service_name = "building-permit-contractor-agent"
    agent_id = "building-permit-contractor-agent"
    agent_display_name = "building_permit_contractor_agent"
    
    print(f"Using Project ID: {project_id}")
    print(f"Using Project Number: {project_number}")
    print(f"Using Region: {region}")
    
    print(f"Retrieving Cloud Run URL for '{service_name}'...")
    service_url = get_cloud_run_url(service_name, region)
    if not service_url:
        print(f"Error: Failed to fetch the URL for service {service_name}")
        sys.exit(1)
    
    agent_card_url = f"{service_url}/a2a/building_permit_contractor_agent/.well-known/agent-card.json"
    print(f"Fetching agent card from: {agent_card_url}")
    
    try:
        req = urllib.request.Request(agent_card_url)
        with urllib.request.urlopen(req) as response:
            agent_card_data = json.loads(response.read().decode("utf-8"))
            spec_content = json.dumps(agent_card_data)
    except URLError as e:
        print(f"Error fetching agent card: {e}")
        sys.exit(1)
        
    with open("contractor-agent.json", "w") as f:
        json.dump(agent_card_data, f, indent=2)
    print("Saved agent card to contractor-agent.json")
    
    print(f"Checking if Agent '{agent_id}' exists in region {region}...")
    check_result = subprocess.run([
        "gcloud", "alpha", "agent-registry", "services", "describe",
        agent_id, "--location", region, "--project", project_id
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if check_result.returncode == 0:
        print(f"Agent '{agent_id}' already exists in region {region}. Skipping creation.")
    else:
        print(f"Agent '{agent_id}' not found. Creating...")
        
        create_args = [
            "gcloud", "alpha", "agent-registry", "services", "create", agent_id,
            f"--project={project_id}",
            f"--display-name={agent_display_name}",
            f"--location={region}",
            "--agent-spec-type=a2a-agent-card",
            f"--agent-spec-content={spec_content}"
        ]
        
        create_result = subprocess.run(create_args)
        if create_result.returncode == 0:
            print(f"Successfully created agent '{agent_id}'.")
        else:
            print(f"Failed to create agent '{agent_id}'.")
            sys.exit(1)

if __name__ == "__main__":
    main()
