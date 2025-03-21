# Use official Python image
FROM python:3.12

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the service port
EXPOSE 5001

# Command to run the service
CMD ["python", "app.py"]

