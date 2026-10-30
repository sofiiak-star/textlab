# Copy to the repository root together with .dockerignore.
FROM python:3.13-slim
WORKDIR /app
COPY analysis.py analyze.py report.py ./
COPY documents/ ./documents/
COPY third_party/ ./third_party/
COPY sources.json LICENSE ./
CMD ["python", "analyze.py", "--help"]
