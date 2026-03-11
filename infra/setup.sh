#!/bin/bash

# Configuration
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT_NAME="build-permit-sa"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
DATA_BUCKET="${PROJECT_ID}-building-permit-data"

echo "Using Project ID: $PROJECT_ID"

# 1. Enable APIs
echo "Enabling necessary APIs..."
APIS=(
  "aiplatform.googleapis.com"
  "documentai.googleapis.com"
  "iam.googleapis.com"
  "serviceusage.googleapis.com"
  "storage.googleapis.com"
  "cloudresourcemanager.googleapis.com"
  "telemetry.googleapis.com"
)

for api in "${APIS[@]}"; do
  echo "Enabling $api..."
  gcloud services enable "$api" --project "$PROJECT_ID"
done

# 2. Create Service Account if it doesn't exist
if ! gcloud iam service-accounts describe "$SERVICE_ACCOUNT_EMAIL" --project "$PROJECT_ID" >/dev/null 2>&1; then
  echo "Creating service account: $SERVICE_ACCOUNT_NAME..."
  gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
    --display-name="Building Permit Compliance SA" \
    --project "$PROJECT_ID"
else
  echo "Service account $SERVICE_ACCOUNT_NAME already exists."
fi

# 3. Assign Roles
echo "Assigning roles to service account..."
ROLES=(
  "roles/aiplatform.user"
  "roles/documentai.apiUser"
  "roles/storage.objectViewer"
  "roles/storage.objectCreator"
  "roles/telemetry.writer"
)

for role in "${ROLES[@]}"; do
  echo "Adding role $role..."
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="$role" >/dev/null
done

# 4. Create GCS Bucket for Database if it doesn't exist
if ! gsutil ls -b "gs://${DATA_BUCKET}" >/dev/null 2>&1; then
  echo "Creating GCS bucket for database: $DATA_BUCKET..."
  gsutil mb -l us-central1 "gs://${DATA_BUCKET}"
else
  echo "GCS bucket $DATA_BUCKET already exists."
fi

echo "Setup script completed successfully."
