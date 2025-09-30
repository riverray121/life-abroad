setup:
	./setup.sh

test:
	PYTHONPATH=$$(pwd) .venv/bin/pytest -q

dev:
	docker compose -f docker-compose.dev.yaml up --build

prod:
	docker compose -f docker-compose.prod.yaml up --build

stop: 
	docker compose -f docker-compose.dev.yaml down
	docker compose -f docker-compose.prod.yaml down

stop-prod:
	docker compose -f docker-compose.prod.yaml down

reset:
	docker compose down -v

freeze:
	pip freeze > requirements.txt