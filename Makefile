WATCH_COMMAND=poetry run uvicorn --reload --port=8000 app.main:app

watch:
	${WATCH_COMMAND}

test:
	poetry run pytest -x -n auto --dist loadscope

retest:
	poetry run pytest -lx --ff -n auto

report:
	poetry run coverage run -m pytest
	poetry run coverage report
	poetry run coverage html

lint:
	poetry run ruff format
	poetry run ruff check --fix

freeze:
	poetry export -f requirements.txt --output build-dependencies.txt --without-hashes

migration:
	poetry run alembic upgrade head
