local-run-app:
	sudo docker compose -f build/docker-compose.yaml --env-file .env up -d --build

local-stop-app:
	sudo docker compose -f build/docker-compose.yaml down --rmi local

prod-run-app:
	docker compose -f build/docker-compose.yaml --env-file prod.env -p seqcraft up -d --build

prod-stop-app:
	docker compose -f build/docker-compose.yaml -p seqcraft down --rmi local
