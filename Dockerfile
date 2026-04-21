# Use official slim Python 3.11 image as base (keeps final size small)
FROM python:3.11-slim as builder

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy requirement and install dependencies into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Start a new, clean stage to keep image size minimal
FROM python:3.11-slim

WORKDIR /app

# Copy over the installed dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code
COPY main.py .
COPY index.html .

# Expose port required by Cloud Run (default: 8080)
EXPOSE 8080

# Command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
