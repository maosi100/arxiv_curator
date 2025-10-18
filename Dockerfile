FROM python:3.13.8-alpine3.22
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --python $(which python3)

COPY src/ ./src/

ENV PYTHONPATH=/app/src/arxiv_curator

CMD ["uv", "run", "src/arxiv_curator/main.py"]
