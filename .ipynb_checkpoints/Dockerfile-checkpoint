# Use a small official Python base image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app with Uvicorn
# --host 0.0.0.0 so it listens inside the container
# --workers 1 for production small API (can scale if needed)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]