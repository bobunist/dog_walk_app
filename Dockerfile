FROM python:3.12-alpine

RUN apk update && apk add --no-cache gcc

WORKDIR /app

COPY . .

COPY build-dependencies.txt .
RUN pip install -r build-dependencies.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ARG WORKERS_COUNT=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
