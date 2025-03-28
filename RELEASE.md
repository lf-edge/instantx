
## Release 2.0.0

Added 
- API for publishing DENM messages
- Synchronization/bridge between MQTT and Kafka for MQTT distribution messages published through API
- Transformation and ASN1 encoding/decoding layer based on NiFi
- AMQP integration through NiFi


Included documentation related with:
- Updated [General documentation](./README.md)
  - [Kafka](./docs/Kafka.md)
  - [NiFi](./docs/Nifi%20ExecuteStreamComand.md)
- [Code of Conduct](./docs/CODE_OF_CONDUCT.md)
- [Contribution](./docs/CONTRIBUTION.md)
- [Maintainers](./docs/MAINTAINERS.md)
- [Security](./docs/SECURITY.md)
- [Support](./docs/SUPPORT.md)
- [License](./LICENSE.md)

Included additional repositories:
- [instantx-metrics](https://github.com/lf-edge/instantx-metrics)
  - HiveMQ Metrics Extension 
- [instantx-connectors](https://github.com/lf-edge/instantx-connectors)
  - Kafka Connectors (MQTT Source and Sink connectors) to be used for Kafka to HiveMQ (and vice-versa) synchronization


## Release 1.0.0

Initial release of with basic MQTT Broker + Observability layer.

### Documentation

Included documentation related with:
- [General documentation](README.md)
  - [MQTT Topic structure](./docs/MQTT-Topic-Structure.md)
  - [UPER Encoding](./docs/Encoding.md)
  - [Geohashes](./docs/Geohashes.md)
  - [ETSI C-ITS Standards](./docs/v2x-messages.md)
- [Deployment](./deployment/Quick-Start.md)
- [License](./LICENSE.md)
