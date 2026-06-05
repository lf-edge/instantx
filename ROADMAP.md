# InstantX Roadmap

This roadmap communicates the project's direction. It is **indicative, not a
commitment** — priorities may shift based on community needs and contributions.
Dated items are reviewed each release. To propose or pick up an item, open a
[GitHub issue](https://github.com/lf-edge/instantx/issues) (see
[CONTRIBUTING.md](./CONTRIBUTING.md)).

_Last reviewed: 2026-06._

## Now (0–3 months)

- **Project quality & supply chain:** reach OpenSSF Best Practices **Silver**
  (CI, ≥80% test coverage, signed releases, threat model). Tracked in
  [docs/planes/openssf-fase2-silver.md](./docs/planes/openssf-fase2-silver.md).
- **Continuous integration:** automated tests, linting (ruff) and SAST (bandit)
  on every pull request.
- **Hardening:** input validation on the Event Publisher API, pinned container
  base images, documented TLS posture.

## Next (3–9 months)

- **Additional C-ITS message types:** extend beyond DENM toward other ETSI
  messages (e.g. CAM, IVIM) across the Event Publisher and NiFi encoder.
- **TLS-by-default deployment profile:** opt-in `docker-compose` overlay with TLS
  enabled for MQTT, Kafka and the API, plus credential management guidance.
- **Observability:** richer Grafana dashboards and exporter metrics.
- **Test coverage growth:** raise coverage toward the OpenSSF **Gold** bar
  (≥90% statement / ≥80% branch).

## Later (9–18 months)

- **OpenSSF Gold:** two-person review on all changes, broader contributor base,
  reproducible builds.
- **Multi-region / federated edge:** patterns for connecting multiple edge
  deployments.
- **Extended integration framework:** more inbound/outbound connectors via NiFi
  beyond AMQP.

## Out of scope (for now)

- Proprietary or closed-source components.
- Re-implementing cryptography in first-party code (TLS is delegated to the
  underlying, configurable infrastructure — see [SECURITY.md](./SECURITY.md)).
