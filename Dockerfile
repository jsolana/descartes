# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install -r /app/requirements.txt

# Set the command to run the application with Uvicorn
CMD ["python", "main.py"]