PY_FILES:=$(shell find . -type f -name '*.py' ! -path './.env/*' ! -path './env/*')

format:
	@poetry run black $(PY_FILES)
	@poetry run isort $(PY_FILES)

create-db:
	@docker run -d \
	--name automl-db \
	-p 80:27017 \
	-e MONGO_INITDB_ROOT_USERNAME=admin \
	-e MONGO_INITDB_ROOT_PASSWORD=1234 \
	mongo:latest
	@make stop-db

reset-db:
	@docker rm automl-db

start-db:
	@docker start automl-db

stop-db:
	@docker stop automl-db

init:
	@make start-db
	@poetry run python main.py
	@make stop-db
