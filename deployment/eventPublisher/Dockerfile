# Use an appropriate base image
FROM python:3.9-alpine

# Install librdkafka and other dependencies
RUN apk add --no-cache \
    librdkafka-dev \
    gcc \
    musl-dev \
    libc-dev \
    linux-headers

# Create a non-root user and group with specific ID for consistency
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port on which the application will run
EXPOSE 5000

# Run the application
CMD ["python", "EventPublisher.py"]
