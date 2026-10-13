# Releases

InstantX uses [Semantic Versioning](https://semver.org/). The notes below summarize the major changes per version; see [CHANGELOG.md](./CHANGELOG.md) for the detailed log.

## Release process & signature verification

A release is cut by pushing a `v*` tag (e.g. `git tag v2.1.0 && git push origin v2.1.0`). The [release workflow](./.github/workflows/release.yml) then builds a source archive and **signs it with [cosign](https://github.com/sigstore/cosign)** — keyless, via GitHub OIDC (no long-lived keys), with the signature recorded in the Sigstore [Rekor](https://docs.sigstore.dev/logging/overview/) transparency log. It attaches the archive, its SHA-256 checksum, the signature (`.sig`), and the signing certificate (`.pem`) to the GitHub Release.

To verify a downloaded release archive:

```bash
cosign verify-blob \
  --certificate "instantx-<version>.tar.gz.pem" \
  --signature "instantx-<version>.tar.gz.sig" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  --certificate-identity-regexp "https://github.com/lf-edge/instantx/.github/workflows/release.yml@.*" \
  "instantx-<version>.tar.gz"
```

The release-manager role is described in [GOVERNANCE.md](./GOVERNANCE.md).

## Upgrade path

Versions follow SemVer: upgrades within the same MAJOR are backward compatible. To upgrade, check out the new tag and rebuild the stack:

```bash
git fetch --tags && git checkout <new-tag>
cd deployment && docker-compose up --build -d
```

Breaking changes (MAJOR bumps) and any required migration steps are called out in the release notes below and in [CHANGELOG.md](./CHANGELOG.md).

## Release 2.3.0

Backward-compatible release. Upgrade note: Kafka Connect registers the MQTT connectors only on first start, so to pick up the new Sink connector setting on an existing stack, recreate it rather than only rebuilding:

```bash
cd deployment && docker-compose down && docker-compose up --build -d
```

The default stack has no persistent volume for Kafka, so this also clears Kafka topics. NiFi named volumes are kept.

Added

- Project website at <https://lf-edge.github.io/instantx/> (`website/`, React + Vite), deployed to GitHub Pages from `main`.
- CodeQL code scanning on pushes, pull requests and weekly, covering the Python services, the website and the GitHub Actions workflows.

Fixed

- The Event Publisher returns `400` instead of `500` for a body with an unknown enumerated value or a string in an integer field.
- On a fresh stack, the first message no longer takes up to 5 minutes to reach MQTT: the MQTT Sink connector now checks for new Kafka topics every 10 seconds instead of every 5 minutes.
- The NiFi scripts' Poetry project resolves again on Python 3.9 and 3.10+, restoring Dependabot security alerts for that package.

Changed

- The NiFi and Kafka speed exporter images install pinned Python dependencies from `requirements.txt` files, so builds are reproducible. The NiFi scripts move to `asn1tools` 0.169.0, matching the Event Publisher (encoded bytes unchanged).
- Event Publisher dependencies updated (`confluent_kafka` 2.15.1, `prometheus_client` 0.26.0, `asn1tools` 0.169.0).
- CI tests each Python component against its pinned requirements; `bandit` findings are uploaded to code scanning; Dependabot applies a cooldown to version updates.

Removed

- The `CLAUDE.md ↔ AGENTS.md` symlink setup; `AGENTS.md` is the only agent-instruction file.

Security

- Event Publisher log sanitisation: untrusted values are stripped of control characters and truncated before logging (CWE-117, CodeQL `py/log-injection`).
- Third-party actions in the release-signing workflow are pinned to commit SHAs.
- `Werkzeug` 3.1.9 ([GHSA-g6x2-hccm-hh4m](https://github.com/pallets/werkzeug/security/advisories/GHSA-g6x2-hccm-hh4m)).

## Release 2.2.0

Backward-compatible release (no migration steps).

Added

- Contributor testing guides: [Manual MQTT Testing](./docs/MQTT-Manual-Testing.md) (broker pub/sub with the `mosquitto` clients) and [HTTP Integration Testing](./docs/HTTP-Integration-Testing.md) (POST to the Event Publisher API and read the message back from MQTT, end-to-end).
- README status badges and an `AGENTS.md` section documenting the `CLAUDE.md ↔ AGENTS.md` symlink setup.

Fixed

- Kafka Connect now starts healthy and exposes its REST API on port 8083 (corrected `CONNECT_REST_ADVERTISED_HOST_NAME`) — resolves #11 and #12.
- The Event Publisher image builds behind restrictive firewalls (base image moved to `python:3.9-slim-bookworm`, dropping the system build toolchain) — resolves #30.

Changed

- Slimmer container bases for the Event Publisher and `nifi-init` images; removed the `linux/amd64` platform pin on the `nifi-setup` service.

## Release 2.1.0

Added

- Community health files (`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `MAINTAINERS.md`), `GOVERNANCE.md`, and `ROADMAP.md`.
- Continuous integration (`ci.yml`): pytest with a ≥80% coverage gate, `ruff`, `bandit`, and a DCO sign-off check; first-party unit tests for the Event Publisher and Kafka speed exporter.
- Keyless release-signing workflow (`release.yml`): every `v*` tag builds a source archive and signs it with cosign (Sigstore).
- Security hardening: allowlist input validation and a request-size limit on the Event Publisher API; `docs/Threat-Model.md` and `docs/Security-Architecture.md`.

Changed

- `EventPublisher.py` refactored into an application factory; encoder/exporter refactored into testable functions (runtime behavior preserved).

Fixed

- NiFi script tests use a path relative to the test file instead of a hardcoded absolute `DATA_FOLDER`.

Security

- Updated Werkzeug (`safe_join` advisories) and pytest (dev) to remediate known CVEs; added Dependabot monitoring.

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
- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Contributing](./CONTRIBUTING.md)
- [Maintainers](./MAINTAINERS.md)
- [Security](./SECURITY.md)
- [Support](./SUPPORT.md)
- [License](./LICENSE.md)

**Security:** No publicly known run-time vulnerabilities were fixed in this release.

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
