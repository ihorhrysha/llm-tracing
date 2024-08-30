# docker compose commands

build:
	docker compose build

up:
	docker compose up app

down:
	docker compose down

make-demo-cluster:
	k3d cluster create k3d-monitoring --servers 1 --kubeconfig-update-default