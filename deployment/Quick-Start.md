[Home](../README.md) > Deployment

# Deploying InstantX - Brokers + Observability + Synchronization + APIs

Contains a package with 4 main layers:

- An **MQTT Broker** (HiveMQ CE)
- An **Apache Kafka broker** and **Kafka Connect** (with 2 MQTT Source and Sink connectors)
- An **Observability layer** (Prometheus + Grafana)
- An **API Service** (Event-Publisher)

## Installation

Run `docker-compose up -d` inside the [deployment](../deployment/) folder
This will run the docker compose file in detached mode and will start all 3 containers (_hivemq ce, prometheus and grafana_)

> If you make any changes to the API Service (Event-Publisher), please run it with the `--build` flag `docker-compose up --build -d`

## Usage

### Ports

We are exposing:

- **Port _1883_** - for MQTT Broker, to be able to send and receive MQTT messages.
- **Port _3000_** - for **Grafana**.
- **Port _9092_** - for Apache Kafka Broker.
- **Port _8083_** - for Kafka Connect API.
- **Port _5000_** - for API Service (Event-Publisher).
- **Port_8090_** - for Nifi console (:8090/nifi).
- **Port_18080_** - for Nifi Registry (:18080/nifi-registry).

### Apache Kafka and Kafka Connect

Please refer to this [documentation](../docs/Kafka.md) for details on how to configure and use Kafka and Kafka Connect.

### Credentials

Inside Grafana, there is a dashboard with standard metrics related to publish/subscribe messages, connection count and connection time.

- **Grafana**
  - <u>Username</u>: _admin_
  - <u>Password</u>: _admin_

### API Service

Please refer to the [documentation](../docs/Event-Publisher-oas.yaml) for details on how to use API Service.

Please refer to this [documentation](../docs/Event-Publisher.md) for details on how to configure and run API Service.

### NIFI

To open Nifi console open localhost:8090/nifi in your browser
To open Nifi Registry console open localhost:18080/nifiregistry in your browser
