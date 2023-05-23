FROM python:3.8-slim

WORKDIR /app

# Install the required Python packages
RUN pip install --no-cache-dir \
    flask \
    pymysql

# Copy the Flask application code to the working directory
COPY . .