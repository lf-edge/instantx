# Use an appropriate base image
# Debian slim: pip installs the prebuilt confluent_kafka wheel, which bundles a
# matching librdkafka. No system librdkafka or C toolchain required.
FROM python:3.9-slim-bookworm

# Create a non-root user and group for consistency
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

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
