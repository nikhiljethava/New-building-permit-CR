.PHONY: setup apis sa rag help

help:
	@echo "Usage:"
	@echo "  make setup   - Run full setup (APIs, SA, IAM, and RAG)"
	@echo "  make apis    - Enable necessary GCP APIs"
	@echo "  make sa      - Create service account and assign roles"
	@echo "  make rag     - Setup RAG engine corpus and upload documents"

setup: apis sa rag

apis:
	@echo "Enabling APIs..."
	./setup.sh # This script currently does both apis and sa, but we can refine if needed

sa:
	@echo "Setting up Service Account..."
	./setup.sh

rag:
	@echo "Setting up RAG Engine..."
	python3 rag_setup.py

chmod:
	chmod +x setup.sh
