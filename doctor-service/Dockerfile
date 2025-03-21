# Use official Python image
FROM python:3.12

# Create non-root user and group with valid home directory
RUN groupadd -r group3 && useradd -r -g group3 -d /home/group3 group3

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Set permissions
RUN mkdir -p /home/group3 && chown -R group3:group3 /app /home/group3

# Switch to non-root user
USER group3

# Install dependencies in user site-packages
RUN pip install --no-cache-dir --user -r requirements.txt

# Expose port
EXPOSE 5002

# Start the app
CMD ["python", "app.py"]

