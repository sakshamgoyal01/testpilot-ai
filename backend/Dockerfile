FROM python:3.11-alpine

# Install build dependencies for common Python packages with C extensions
# These are crucial for many common packages to compile correctly on Alpine
RUN apk add --no-cache build-base python3-dev \
  && rm -rf /var/cache/apk/* # Clean up apk cache to reduce image size

WORKDIR /app

# Copy requirements.txt first to leverage Docker's build cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your API will run on
EXPOSE 8000

# Command to run your Uvicorn application
# Replace 'main:app' with the actual entry point of your FastAPI/ASGI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]