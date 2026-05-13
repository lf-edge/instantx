[Home](../README.md) > API Service (Even-Publisher)

## Overview

Event Publisher is a service designed to ingest DENM (Decentralized Environmental Notification Messages) data through APIs from an external provider and publish them to Kafka.

## Features

- **Data Ingestion**: Connects to external APIs to fetch DENM/IVIM data.
- **Kafka Integration**: Publishes ingested data to a Kafka topic for further processing.

## Prerequisites

- **Kafka**: Ensure you have a Kafka cluster set up and running.

## Dependencies

Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Update the `eventPublisher/config.py` file with your API credentials and Kafka configuration:

    ```python
    # Address of the Kafka broker, which is the server that manages the Kafka cluster.
    KAFKA_BROKER = 'kafka:9092'

    # The Kafka topic where DENM/IVIM data will be published.
    KAFKA_TOPIC = 'v2x.denm.public'

    # Port number for the Prometheus server, used for monitoring and metrics.
    PROMETHEUS_SERVER = 8000

    # Port number on which the Event Publisher service will run.
    port = 5000

    # Name of the metric that tracks the count of incoming messages.
    MESSAGES_COUNT_METRICS = 'incoming_messages'
    ```

You can also run the service directly in your local Python environment we to do that you will change `eventPublisher/config.py` file to set host and port for `KAFKA_BROKER` to connect outside from Docker.

```bash
python eventPublisher/EventPublisher.py
```
