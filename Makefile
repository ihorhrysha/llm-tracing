VERSION=$(shell git describe --tags --abbrev=0)-$(shell git rev-parse --short HEAD)

# Defaults
REGISTRY = ghcr.io
REPOSITORY = ihorhrysha/llm-tracing
IMAGE_TAG = ${REGISTRY}/${REPOSITORY}:${VERSION}


# docker compose commands

build:
	docker compose build

up:
	docker compose up app

down:
	docker compose down

make-demo-cluster:
	k3d cluster create k3d-monitoring --servers 1 --kubeconfig-update-default

# release commands

version:
	@echo ${VERSION}

image:
	docker build . -t ${IMAGE_TAG} 

push:
	docker push ${IMAGE_TAG}

clean:
	docker rmi ${IMAGE_TAG} || true

release: image push clean