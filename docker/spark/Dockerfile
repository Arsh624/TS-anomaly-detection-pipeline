# --- Stage 1: Build a Python environment with dependencies ---
FROM python:3.11-slim as python_deps_builder

# Set up a working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies into a custom directory
RUN pip install --no-cache-dir --target=/app/python_deps -r requirements.txt


# --- Stage 2: Build the final Spark application image ---
FROM bitnami/spark:3.5.1

# Copy the dependencies from the builder stage
COPY --from=python_deps_builder /app/python_deps /opt/bitnami/spark/python_deps

# Set the PYTHONPATH environment variable permanently in the image
ENV PYTHONPATH=/opt/bitnami/spark/python_deps:$PYTHONPATH