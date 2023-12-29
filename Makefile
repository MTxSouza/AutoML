PY_FILES:=$(shell find . -type f -name '*.py' ! -path './.env/*' ! -path './env/*')

format:
	@poetry run black $(PY_FILES)
	@poetry run isort $(PY_FILES)

run-db:
	@docker run -d --rm \
	--name automl-db \
	-p 80:27017 \
	-e MONGO_INITDB_ROOT_USERNAME=admin \
	-e MONGO_INITDB_ROOT_PASSWORD=1234 \
	mongo:latest

stop-db:
	@docker stop automl-db
