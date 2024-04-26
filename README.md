# InstantX UC1 - HiveMQCE + Observability

We have a package of 3 components: HiveMQ CE, Prometheus and Grafana

## Installation

docker-compose up -d - This will run the docker compose file in detached mode and will start the hivemq ce, prometheus and grafana containers

## Usage
We are exposing port 1883 for the HiveMQ CE, to be able to send and receive MQTT messages.
We are exposing port 3000 for grafana (http://localhost:3000). Inside grafana there is a dashboard with few metrics related to publish/subscribe messages, connection count and connection time