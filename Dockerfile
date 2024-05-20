# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install reportlab
RUN pip install reportlab

# Copy the current directory contents into the container at /app
COPY . /app

# Specify the command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]