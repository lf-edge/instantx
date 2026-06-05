# Development Guide

This guide describes how to build, run, test, lint, and statically analyze the **first-party** code in this repository. InstantX is primarily a deployment-and-integration project: an off-the-shelf broker/observability stack orchestrated with `docker-compose`, glued together by first-party Python services and scripts plus an Apache NiFi flow.

First-party Python lives in:

- [`deployment/eventPublisher`](../deployment/eventPublisher) — the Flask Event Publisher API.
- [`deployment/kafka_speed_exporter`](../deployment/kafka_speed_exporter) — a Prometheus exporter.
- [`deployment/nifi/nifi-scripts`](../deployment/nifi/nifi-scripts) — the NiFi encoder/decoder scripts (Poetry project, with the test suite).

## Build

The full platform is built and run with Docker Compose. All commands run from `deployment/`:

```bash
# Build images and start the stack
docker-compose up --build -d

# Start without rebuilding
docker-compose up -d

# Tear down
docker-compose down
```

The NiFi scripts package is a standard [Poetry](https://python-poetry.org/) project:

```bash
cd deployment/nifi/nifi-scripts
poetry install            # installs runtime + dev dependencies
```

The Event Publisher uses a pinned `requirements.txt`:

```bash
cd deployment/eventPublisher
pip install -r requirements.txt
```

All build and analysis tools used here are free/libre and open source (Docker, Poetry, pytest, ruff, bandit).

## Test

The first-party automated test suite uses [pytest](https://docs.pytest.org/) and lives in the NiFi scripts package:

```bash
cd deployment/nifi/nifi-scripts
poetry run pytest                              # run the suite
poetry run pytest -s --cov=src --cov-report=xml  # with coverage
```

### Testing policy

Major new functionality **must** be accompanied by automated tests, and bug fixes should add a regression test where practical. This policy is stated in [CONTRIBUTING.md](../CONTRIBUTING.md#testing-policy) and reinforced by a checklist item in the [pull request template](../.github/PULL_REQUEST_TEMPLATE.md).

## Lint (ruff)

Python code is linted with [ruff](https://docs.astral.sh/ruff/). The shared configuration lives in
[`deployment/nifi/nifi-scripts/pyproject.toml`](../deployment/nifi/nifi-scripts/pyproject.toml) under `[tool.ruff]`.

Run it across all first-party Python from the repository root:

```bash
ruff check \
  deployment/eventPublisher \
  deployment/kafka_speed_exporter \
  deployment/nifi/nifi-scripts \
  --config deployment/nifi/nifi-scripts/pyproject.toml
```

`ruff` is available as a Poetry dev dependency in the NiFi scripts package (`poetry run ruff ...`) or as a standalone tool (`pipx install ruff` / `uvx ruff`).

## Static analysis (bandit)

Python code is scanned for common security issues with [bandit](https://bandit.readthedocs.io/) before each major release:

```bash
bandit -r \
  deployment/eventPublisher \
  deployment/kafka_speed_exporter \
  deployment/nifi/nifi-scripts/src
```

`bandit` is available as a Poetry dev dependency in the NiFi scripts package (`poetry run bandit ...`) or standalone (`pipx install bandit`). Findings of medium severity or higher are addressed (fixed or, where a finding is a false positive, suppressed with a justifying comment) before release.

## Before opening a pull request

1. `poetry run pytest` passes (add/update tests for your change).
2. `ruff check ... --config deployment/nifi/nifi-scripts/pyproject.toml` reports no errors.
3. `bandit -r ...` reports no unaddressed medium-or-higher findings.
4. Update [CHANGELOG.md](../CHANGELOG.md) for user-facing changes.
