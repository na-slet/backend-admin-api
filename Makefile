include .env
export

ALEMBIC = database

shell:
	poetry shell

prepare:
	poetry install || true

run:
	poetry run uvicorn api.__main__:app --host 0.0.0.0 --port ${FASTAPI_PORT} --log-level critical

clear:
	docker kill na-slet-creator-api || true

build:
	docker build -t na-slet-creator-api --no-cache .

run-docker:
	docker container rm na-slet-creator-api || true
	docker run --name na-slet-creator-api -d -p ${FASTAPI_PORT}:${FASTAPI_PORT} --restart always --network na-slet-network na-slet-creator-api
