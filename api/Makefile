.PHONY: install start build clean

install:
	go mod download

start:
	go run main.go

build:
	go build -o api-server main.go

clean:
	rm -f api-server

deploy:
	gcloud builds submit --config .cloudbuild/deploy.yaml --substitutions _COMMIT_SHA=$(shell git rev-parse --short HEAD) .
