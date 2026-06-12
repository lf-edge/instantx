# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- Project landing page (`website/`, React + Vite) deployed to GitHub Pages via `.github/workflows/website.yml` (<https://lf-edge.github.io/instantx/>).

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