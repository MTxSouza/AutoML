PY_FILES:=$(shell find . -type f -name '*.py' ! -path './.env/*' ! -path './env/*')

format:
	@poetry run black $(PY_FILES)
	@poetry run isort $(PY_FILES)

run:
	@poetry run uvicorn server.app:app --reload