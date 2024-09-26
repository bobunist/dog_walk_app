#!/bin/sh

WORKERS_COUNT=${WORKERS_COUNT:-1}

alembic upgrade head

exec gunicorn src.main:app --worker-class uvicorn.workers.UvicornWorker --workers "$WORKERS_COUNT" --bind 0.0.0.0:8000
