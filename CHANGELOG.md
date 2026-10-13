# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.3.0] - 2026-10-14

### Added

- Project landing page (`website/`, React + Vite, linted with `oxlint`) at <https://lf-edge.github.io/instantx/>, built on pull requests and deployed to GitHub Pages from `main` by `.github/workflows/website.yml`. It includes a panel linking the LF Edge Slack channel. The README links the site and adds Website and CodeQL status badges.
- CodeQL code scanning (`.github/workflows/codeql.yml`) on every push to `main`, every pull request, and weekly. Analyses run the `security-extended` query suite over the Python services, the React/Vite website, and the GitHub Actions workflows themselves; results appear as code scanning alerts under the repository's Security tab.

### Changed

- `bandit` now emits SARIF and uploads it to code scanning, so Python SAST findings are tracked as alerts (with dedup and dismissal history) instead of only failing the CI check. The check still fails the build on any finding.
- Dependabot now applies a conservative `cooldown` to version updates: 30 days for major, 14 for minor and 7 for patch releases (14 days for GitHub Actions, which supports only `default-days`). New releases soak before adoption, giving yanked releases and supply-chain issues time to surface. Security updates are unaffected and still open pull requests immediately.
- The NiFi and Kafka speed exporter images install pinned Python dependencies from new `requirements.txt` files (`deployment/nifi/` and `deployment/kafka_speed_exporter/`), both tracked by Dependabot. Previously they installed whatever version was latest at build time, so two machines could run different library versions, depending on their Docker build cache.
- The NiFi scripts now use `asn1tools` 0.169.0 (was 0.167.0), the same version as the Event Publisher. It removes the pyparsing deprecation warnings 0.167.0 emitted; the encoded bytes are unchanged.
- CI runs each Python test suite in its own virtualenv built from the component's pinned requirements file, instead of one environment with unpinned packages. Dependabot bumps are now tested against the version that actually ships, including `confluent_kafka`, which CI previously did not install at all.
- Event Publisher runtime dependencies: `confluent_kafka` 2.14.2 → 2.15.1, `prometheus_client` 0.25.0 → 0.26.0 and `asn1tools` 0.167.0 → 0.169.0 (`Werkzeug` is listed under Security).
- CI uses `actions/checkout` v7 and `actions/setup-python` v7.

### Removed

- The Claude Code-specific instruction-file setup: the symlink instructions in `AGENTS.md` and the matching `.gitignore` entries. The repository follows the [AGENTS.md](https://agents.md) standard, with `AGENTS.md` as its only agent-instruction file.

### Fixed

- Event Publisher returns `400` instead of `500` for a body with an unknown enumerated value (e.g. `"altitudeConfidence": "nope"`) or a string in an integer field. `asn1tools` raises `KeyError`/`TypeError` for these rather than `EncodeError`, which was the only error handled.
- On a fresh stack, the first message no longer takes up to 5 minutes to reach MQTT. `v2x.denm.public` is created by the first POST, after the MQTT Sink connector has subscribed to `topics.regex`, and the connector only discovered new matching topics on its default 5-minute metadata refresh. It now refreshes every 10 s (`consumer.override.metadata.max.age.ms`). The connector config is registered on first start only, so an existing stack picks this up after `docker-compose down && docker-compose up -d`.
- The NiFi scripts' Poetry project (`deployment/nifi/nifi-scripts`) resolves again. `pytest` 9.x and `bandit` 1.9.x require Python 3.10+, while the project supports 3.9+, so `poetry install` failed and GitHub's dependency graph for this package was degraded, which meant Dependabot security alerts were not generated for it. The two tools now declare a version per Python range, `poetry.lock` is committed, and a `poetry-lock` CI job (`poetry check --lock`) catches a recurrence.

### Security

- Untrusted values are sanitised before being written to the Event Publisher log: control characters (including CR and LF) are stripped and values longer than `LOG_VALUE_MAX_LENGTH` (optional in `config.py`, default 256) are truncated. This closes CodeQL alert `py/log-injection` (CWE-117) and, more importantly, hardens the ASN.1 encoding-error path, where field names and values from an otherwise unvalidated request body reached the log and could have been used to forge log entries.
- The release-signing workflow pins its third-party actions (`sigstore/cosign-installer`, `softprops/action-gh-release`) to full commit SHAs instead of mutable tags. The job holds `contents: write` and `id-token: write`, so a compromised upstream tag could otherwise have run code able to publish and sign releases. Dependabot keeps the SHAs current. This resolves the CodeQL `actions/unpinned-tag` alerts.
- Event Publisher `Werkzeug` 3.1.8 → 3.1.9, a security release that fixes [GHSA-g6x2-hccm-hh4m](https://github.com/pallets/werkzeug/security/advisories/GHSA-g6x2-hccm-hh4m) (`safe_join` and Windows device names; the shipped image is Linux-based).

## [2.2.0] - 2026-06-22

### Added

- `docs/MQTT-Manual-Testing.md` — connect to the local HiveMQ broker and validate the publish/subscribe flow with the `mosquitto` clients; linked from the README and `CONTRIBUTING.md`.
- `docs/HTTP-Integration-Testing.md` — POST a V2X (DENM) message to the Event Publisher API and read it back from MQTT, covering the HTTP → Kafka → MQTT path end-to-end; linked from the README and `CONTRIBUTING.md`.
- Status badges (CI, release, cosign, license, Python, `ruff`, `bandit`) in the README.
- Section in `AGENTS.md` documenting the `CLAUDE.md ↔ AGENTS.md` symlink setup.

### Changed

- Event Publisher image base changed from `python:3.9-alpine` to `python:3.9-slim-bookworm`, relying on the prebuilt `confluent_kafka` wheel (bundled `librdkafka`) instead of compiling against a system toolchain.
- `nifi-init` image base changed from `ubuntu:latest` to `alpine:3.20` (installing `bash`, `curl`, `jq` via `apk`) and removed the now-unneeded `linux/amd64` platform pin on the `nifi-setup` service.

### Fixed

- Kafka Connect `CONNECT_REST_ADVERTISED_HOST_NAME` corrected from `kafka` to `connect`, so the container healthcheck and inter-worker REST calls reach the right host; the worker now becomes healthy and the REST API on port 8083 is reachable (#11, #12).
- Event Publisher image build no longer fails behind restrictive firewalls — the failing `apk add librdkafka-dev gcc musl-dev libc-dev linux-headers` step was removed with the base-image change (#30).

### Security

- Dependency updates via Dependabot: `actions/checkout`, `actions/setup-python`, `softprops/action-gh-release`, and the `ruff` dev dependency.

## [2.1.0] - 2026-06-05

### Added

- Root-level `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, and `MAINTAINERS.md` for standard discoverability (GitHub community health files).
- `docs/Development.md` describing build, test, lint (`ruff`), and static analysis (`bandit`) workflows.
- `.github/` pull request and issue templates.
- `ruff` (linting) and `bandit` (static analysis) configuration for first-party Python code.
- OpenSSF Best Practices badge in the README.
- Continuous integration (`.github/workflows/ci.yml`): pytest with a ≥80% coverage gate, `ruff`, `bandit`, and a DCO sign-off check on every pull request.
- Unit tests for the Event Publisher API and the Kafka speed exporter (first-party coverage ≥80%).
- Allowlist input validation and a request-size limit on the Event Publisher API.
- `GOVERNANCE.md`, `ROADMAP.md`, `docs/Threat-Model.md`, and `docs/Security-Architecture.md`.
- Developer Certificate of Origin (DCO) sign-off requirement (documented in `CONTRIBUTING.md`, enforced in CI).
- Release-signing workflow (`.github/workflows/release.yml`): on every `v*` tag, builds a source archive and signs it with cosign (keyless, Sigstore) before publishing a GitHub Release.

### Changed

- Moved governance documentation from `docs/` to the repository root and fixed internal links.
- Rewrote `SUPPORT.md` (previously a duplicate of the contribution guide) with real support channels.
- Refactored `EventPublisher.py` into an application factory and `encoder_decoder.py`/`kafka_speed_exporter.py` into testable functions (runtime behavior preserved).
- Documented signed-release verification (Sigstore `gitsign`) and the upgrade path in `RELEASE.md`.

### Fixed

- Replaced a hardcoded absolute `DATA_FOLDER` path in the NiFi script tests with a path relative to the test file, so the suite runs on any machine.

### Security

- Updated Werkzeug to 3.1.6 to remediate the moderate `safe_join` Windows device-name advisories (CVE-2025-66221, CVE-2026-21860, CVE-2026-27199).
- Updated pytest (dev dependency) to 9.0.3 to remediate the tmpdir handling advisory (CVE-2025-71176).
- Added `.github/dependabot.yml` to monitor dependencies for future advisories.
- No publicly known run-time vulnerabilities affect the first-party code itself.

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
