# InstantX Threat Model & Assurance Case

This document is the project's **assurance case**: it states what InstantX is
expected to protect, the trust boundaries in the system, the main threats at
each boundary, and how the design mitigates them. It is reviewed as the
architecture evolves. See also [Security-Architecture.md](./Security-Architecture.md)
and [SECURITY.md](../SECURITY.md).

## Scope

InstantX is a deployment-and-integration platform: a `docker-compose` stack of
off-the-shelf brokers and observability tools, glued together by first-party
code (the Event Publisher API, the NiFi encoder/decoder scripts, and a metrics
exporter). This model covers the **first-party code and the reference
deployment**; operators are responsible for hardening their own production
environment.

## Assets

- **Integrity and availability** of V2X (C-ITS) messages flowing through the
  pipeline — incorrect or dropped messages can affect downstream road-safety use.
- **Availability** of the ingestion API and brokers.
- **Operator credentials** for the brokers, Grafana, and any external systems.

## Trust boundaries & data flow

```
[External publisher] --HTTP--> (1) Event Publisher API (Flask)
        --> Kafka (v2x.denm.public) --> Kafka Connect (MQTT source/sink)
        --> (2) MQTT broker (HiveMQ CE) --> [Subscribers]

[External AMQP/RabbitMQ] --> (3) Apache NiFi (transform + UPER encode) --> brokers

(4) Prometheus/Grafana <-- metrics from services
```

Trust boundaries (where data crosses from less-trusted to more-trusted):
1. **Untrusted client → Event Publisher API** — arbitrary HTTP input.
2. **Edge ↔ broker network** — messages in transit between components and to subscribers.
3. **External AMQP source → NiFi** — externally-supplied payloads.
4. **Operator ↔ observability/admin UIs** — Grafana, NiFi, Kafka Connect consoles.

## Threats and mitigations (STRIDE per boundary)

| # | Boundary | Threat (STRIDE) | Mitigation |
|---|----------|-----------------|------------|
| 1 | Client → API | **Tampering / DoS** via malformed or oversized bodies | Allowlist validation of `sub_service`, `sub_service_group`, and `geohash`; request size limit (`MAX_CONTENT_LENGTH`); schema-driven UPER encoding rejects non-conforming payloads with HTTP 400. |
| 1 | Client → API | **Spoofing / Elevation** | API performs no privileged action beyond producing to Kafka; deployments SHOULD place the API behind an authenticating gateway/TLS terminator (operator responsibility). |
| 2 | In transit | **Information disclosure / MITM** | Transport is delegated to the brokers' standard TLS (MQTT/Kafka) and HTTPS; operators enable TLS 1.2+ and certificate verification (see Security-Architecture). |
| 3 | AMQP → NiFi | **Tampering** via malformed external messages | NiFi flow normalizes/validates types before UPER encoding; the encoder rejects non-conforming input. |
| 4 | Admin/observability | **Spoofing / Elevation** via default credentials | Default credentials (e.g. Grafana `admin/admin`) are documented as **development-only** and MUST be changed before production ([Quick-Start.md](../deployment/Quick-Start.md)). |
| all | Supply chain | **Tampering** via vulnerable dependencies | Pinned dependencies + Dependabot monitoring; `bandit` SAST and `ruff` lint in CI; container base images pinned. |

## Assumptions

- Operators run the stack inside a controlled network and enable TLS and
  non-default credentials for any non-local deployment.
- First-party code does **not** implement cryptography; confidentiality and
  integrity in transit rely on the configurable TLS of the underlying components.
- The brokers and tools (HiveMQ, Kafka, NiFi, Grafana, Prometheus) are trusted,
  off-the-shelf components kept up to date by the operator.

## Residual risk

Within the reference (local) deployment, TLS and authentication are **opt-in**.
Running it as-is on an untrusted network is out of scope and explicitly
discouraged. Production hardening is the operator's responsibility, guided by
[Security-Architecture.md](./Security-Architecture.md).
