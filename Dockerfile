# Secure container defaults for the Team Notes demo.
# Compare with learning/broken_app/Dockerfile to see insecure patterns.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    NOTES_DB_PATH=/data/notes.db

WORKDIR /app

# Install dependencies as root, then drop privileges for runtime.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /data /app

COPY app ./app

USER appuser

EXPOSE 5000

CMD ["python", "-m", "app.main"]
