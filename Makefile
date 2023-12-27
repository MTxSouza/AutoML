PY_FILES:=$(shell find . -type f -name '*.py' ! -path './.env/*' ! -path './env/*')

format:
	@poetry run black $(PY_FILES)
	@poetry run isort $(PY_FILES)

build_dependencies:
	@poetry export -f requirements.txt --with db,api,ml -o requirements/base.txt --without-hashes
	@poetry export -f requirements.txt --with dev -o requirements/dev.txt --without-hashes

run:
	@poetry run uvicorn server.app:app --reload

test:
	@poetry run pytest --disable-warnings