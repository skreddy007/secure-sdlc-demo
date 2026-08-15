# INTENTIONAL insecure Dockerfile for learning.
# Problems: runs as root, uses an older base tag pattern, debug-friendly defaults.

FROM python:3.11

WORKDIR /app
COPY requirements-broken.txt .
RUN pip install -r requirements-broken.txt
COPY app.py .

# Runs as root (no USER directive) — container escape impact is higher.
EXPOSE 5000
CMD ["python", "app.py"]
