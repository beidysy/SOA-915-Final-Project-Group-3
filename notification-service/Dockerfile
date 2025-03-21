# Use official Python image
FROM python:3.12

# Create a non-root user and group
RUN groupadd -r group3 && useradd -r -g group3 group3

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set permissions for the working directory
RUN chown -R group3:group3 /app

# Switch to non-root user
USER group3

# Expose the service port
EXPOSE 5004

# Command to run the service
CMD ["python", "app.py"]

