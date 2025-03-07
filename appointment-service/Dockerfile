# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the service runs on
EXPOSE 5003

# Define the command to run the application
CMD ["python", "app.py"]
