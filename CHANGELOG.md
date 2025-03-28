# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

...

## 2.0.0 - 2025-03-28

### Added

- .github folder containing Pull Request Template and Issue Template files
- CODE_OF_CONDUCT.md
- MAINTANERS.md
- SECURITY.md
- SUPPORT.md
- CHANGELOG.md
- Event Publisher (API Service)
- Kafka Connect (MQTT Source and Sink) connectors
- HiveMQ Metrics Extension (source code)
- ...

### Changed

- CONTRIBUTION file updated with details on how to contribute with source code.
- README file changed to include additional UseCase for InstantX.
- Deployment folder and docker-compose updated to include new components (API Service, Apache Kafka, Kafka Connect and Apache Nifi)
- Changelog to reflext these changes

## 1.0.0 - 2024-05-03

### Added

- CONTRIBUTION, LICENSE, README and RELEASE files (1st versions)
- Documentation folder containing MQTT topic structure, geohashes structure and encodings used
- Deployment instructions and docker-compose file to start a full platform instance
- Observability dashboards (for Grafana)
- HiveMQ Extensions (artifacts - no source code yet)