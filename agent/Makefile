.PHONY: install start build clean

install:
	uv sync

start:
	uv run uvicorn main:app --reload --port 8000

build:
	@echo "Python builds are typically just dependencies, use 'make install'"

clean:
	rm -rf .venv
