FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN uv sync --frozen --no-dev

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]