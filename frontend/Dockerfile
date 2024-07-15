# Use the official Python image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install Flask
RUN pip install Flask

# Copy the entire frontend directory into the Docker image
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
