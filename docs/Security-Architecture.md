# InstantX Security Architecture

This document records the project's **security requirements and expectations**,
the secure-design principles it follows, and operator guidance for hardening a
deployment. It complements the [Threat Model](./Threat-Model.md) and the
disclosure process in [SECURITY.md](../SECURITY.md).

## Security requirements & expectations

- The Event Publisher API **validates all untrusted input** before use.
- First-party code contains **no secrets**; credentials are supplied at runtime
  via environment variables / `.env` files (which are git-ignored).
- Components support **TLS 1.2+** for network communication, configured by the operator.
- Known dependency vulnerabilities of medium+ severity are **patched promptly**
  (monitored by Dependabot; see [CHANGELOG.md](../CHANGELOG.md)).

## Secure-design principles applied

- **Input validation (allowlist):** `sub_service`, `sub_service_group`, and
  `geohash` are validated against allowlists/patterns in
  [`EventPublisher.py`](../deployment/eventPublisher/EventPublisher.py); payloads
  must conform to the ASN.1 schema or are rejected with HTTP 400.
- **Least privilege:** service containers run as **non-root** users (e.g.
  `appuser` in the Event Publisher image, `nifi` in the NiFi image).
- **Fail-safe defaults:** secrets are excluded via `.gitignore`; default
  credentials are clearly flagged to be changed before production.
- **Limited attack surface:** the API exposes a single publish endpoint and
  performs no privileged operations beyond producing to Kafka.
- **Defense in transit:** transport security is delegated to standard,
  well-reviewed TLS implementations in the brokers/HTTP layer.

## Cryptography posture

InstantX first-party code does **not** implement or directly use cryptographic
algorithms (UPER/ASN.1 is encoding, not cryptography). Where confidentiality or
integrity in transit is required, it is provided by the **configurable TLS** of
the underlying components:

- **`crypto_used_network` / TLS 1.2+:** MQTT (HiveMQ), Kafka, and the HTTP API
  all support TLS 1.2+; enable it per the component's documentation.
- **Certificate verification:** when TLS is enabled, clients MUST verify server
  certificates by default (do not disable verification).
- **Credential agility:** credentials and keys are provided via configuration
  (environment variables / `.env` / broker config), so they can be rotated
  **without recompiling or rebuilding** first-party code.

## Operator hardening checklist (production)

- [ ] Change **all default credentials** (Grafana, brokers, NiFi, Registry).
- [ ] Enable **TLS 1.2+** on MQTT, Kafka, and the API; verify certificates.
- [ ] Place the Event Publisher API behind an **authenticating gateway** / TLS terminator.
- [ ] Restrict network exposure of admin/observability ports (Grafana 3000,
      NiFi 8090, Kafka Connect 8083, Registry 18080) to trusted networks.
- [ ] Supply secrets via environment / secret manager, never committed to git.
- [ ] Keep dependencies and container base images updated (Dependabot is enabled).

## Build & supply-chain integrity

- Python dependencies are **version-pinned**; Dependabot opens update PRs.
- CI runs **ruff** (lint) and **bandit** (SAST) on every pull request, and
  enforces ≥80% test coverage ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)).
- Release tags are **cryptographically signed** (Sigstore `gitsign`); see
  [RELEASE.md](../RELEASE.md) for the verification process.
- Container base images are pinned to reduce build drift.
