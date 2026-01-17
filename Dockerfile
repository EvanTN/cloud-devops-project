FROM python:3.11-slim

# Install system dependencies (curl for HEALTHCHECK)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure entrypoint is executable
RUN chmod +x entrypoint.sh

# Fix permissions so non-root user can access files
RUN chown -R app:app /app

# Switch to non-root user
USER app

EXPOSE 8000

CMD ["./entrypoint.sh"]

HEALTHCHECK --interval=60s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
