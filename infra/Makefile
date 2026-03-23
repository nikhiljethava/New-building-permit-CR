.PHONY: setup apis sa rag agent-engine artifact-registry help

help:
	@echo "Usage:"
	@echo "  make setup   - Run full setup (APIs, SA, IAM, AR, and RAG)"
	@echo "  make apis    - Enable necessary GCP APIs"
	@echo "  make sa      - Create service account and assign roles"
	@echo "  make artifact-registry - Create Artifact Registry repository"
	@echo "  make rag     - Setup RAG engine corpus and upload documents"
	@echo "  make agent-engine - Deploy the Vertex AI Agent Engine"

setup: apis sa artifact-registry rag agent-engine

apis:
	@echo "Enabling APIs..."
	./setup.sh

sa:
	@echo "Setting up Service Account..."
	./setup.sh

artifact-registry:
	@echo "Setting up Artifact Registry..."
	./setup.sh

rag:
	@echo "Setting up RAG Engine..."
	python3 rag_setup.py

agent-engine:
	@echo "Deploying Agent Engine..."
	cd ../agent-engine && make deploy

chmod:
	chmod +x setup.sh
