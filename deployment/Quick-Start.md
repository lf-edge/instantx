
[Home](../README.md) > Deployment

# Deploying InstantX UC1 - MQTT Broker + Observability

Contains a package with 3 main components: an **MQTT Broker** (HiveMQ CE) and **Observability layer** (Prometheus + Grafana)

## Installation

Run `docker-compose up -d` inside the [deployment](../deployment/) folder
This will run the docker compose file in detached mode and will start all 3 containers (*hivemq ce, prometheus and grafana*)

## Usage
### Ports
We are exposing:
- **Port *1883*** - for MQTT Broker, to be able to send and receive MQTT messages.
- **Port *3000*** - for **Grafana**.

### Credentials
Inside Grafana, there is a dashboard with standard metrics related to publish/subscribe messages, connection count and connection time.
- **Grafana**
  - <u>Username</u>: *admin*
  - <u>Password</u>: *admin*
