# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Upgrade pip and install the dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose port 8000 to allow external access
EXPOSE 8000

# Run the FastAPI app using uvicorn when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
