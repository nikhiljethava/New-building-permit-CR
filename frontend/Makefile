.PHONY: install start build clean

install:
	npm install

start:
	npm run dev

build:
	npm run build

clean:
	rm -rf node_modules dist

deploy:
	gcloud builds submit --config .cloudbuild/deploy.yaml --substitutions _COMMIT_SHA=$(shell git rev-parse --short HEAD) .
