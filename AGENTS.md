# InstantX (LF Edge) - Agent Instructions

> **Setup:** This file is the single, version-controlled source of agent instructions. Claude Code reads `CLAUDE.md`, which is git-ignored on purpose — symlink it to this file after cloning. See [section 8](#8-agent-instruction-files-claudemd--agentsmd).

## 1. Agent Persona & Operational Guidelines
- **Assigned Role:** Technical assistant operating under the strict guidelines of a Cloud Solution Architect and Tech Lead PO.
- **Tone and Style:** Concise, direct, and rigorously professional.
- **Strict Accuracy (Zero Hallucinations):** If the source code, tests, or documentation lack specific details, explicitly state the missing information. Do not assume or invent paths, variables, or logic.
- **Design Approach:** Prioritize cloud-native architectural decisions, distributed resilience, low-latency edge processing, and adherence to ETSI/5GAA industry standards.

## 2. Project Overview
**InstantX** (InstantX) is an LF Edge / Vodafone Business edge-cloud platform for real-time, location-addressed data exchange, focusing on **V2X** (Vehicle-to-Everything) C-ITS messaging. 

It is a deployment-and-integration repository: a `docker-compose` stack of off-the-shelf brokers and observability tools, glued together by first-party code (Python services + scripts + a NiFi flow). 
- **Core Mechanism:** Messages are addressed by **geohash** so subscribers receive only data for their location and radius. 
- **Transport & Routing:** MQTT is the edge transport; Kafka is the internal backbone; NiFi is the transformation/integration layer.
- **Primary Directories:** `deployment/` (infrastructure and code), `docs/` (conceptual reference).

## 3. Message Pipeline Architecture
Understanding the system requires tracing a message end-to-end:

1. **Ingress (Event Publisher):** A Flask API (`deployment/eventPublisher/EventPublisher.py`). Receives a V2X JSON body, UPER-encodes it via `asn1tools`, and produces it to Kafka topic `v2x.denm.public`. The geohash is exploded into an MQTT-style key (`v2x/<sub_service>/<group>/g<level>/<g/e/o/h/a/s/h>`) and set as the **Kafka message key**.
2. **Transport Bridge (Kafka Connect):** Custom MQTT Source/Sink connectors synchronize messages bidirectionally between MQTT and Kafka **without transforming the payload**. They translate the MQTT geohash topic structure to the flat Kafka topic name, preserving the geohash path as the Kafka key.
3. **Transformation (Apache NiFi):** Consumes from external systems (e.g., AMQP/RabbitMQ), transforms, and re-publishes. Key logic is in `deployment/nifi/nifi-scripts/src/encoder_decoder.py` (reads XML on stdin, normalizes types, UPER-encodes, writes hex to stdout).
4. **Egress (MQTT broker - HiveMQ CE):** Subscribers use geohash wildcards on the topic tree to receive local messages.

### Topic / Key Convention (Critical)
- **MQTT topic:** `{service}/{subService}/{subServiceGroup}/g{level}/{geohash char-by-char}` (e.g., `v2x/denm/public/g8/7/y/0/1/9/1/k/4`).
- **Kafka topic:** Dotted, geohash-free (e.g., `v2x.denm.public`). The full geohash topic path travels exclusively as the Kafka **key**.

## 4. V2X Encoding Details
Messages follow **ETSI C-ITS** standards encoded with **UPER** (Unaligned Packed Encoding Rules) from ASN.1 schemas. 

- **Multi-part Encoding Warning:** A full `DenmEtsi` message is NOT encoded in one call in NiFi. `encoder_decoder.py` encodes three parts separately (GeoNetworking header, BTP-B header, inner DENM), computes the `payloadLength`, and concatenates them. The Event Publisher uses a simpler single-call path; **do not assume they encode identically.**

## 5. Commands & Operations
All commands run from `deployment/` unless noted.

### Docker Infrastructure
`docker-compose up -d`
`docker-compose up --build -d`
`docker-compose down`

### Python Scripts (NiFi)
Managed via Poetry in `deployment/nifi/nifi-scripts`:
`poetry install`
`poetry run pytest`

### Event Publisher (Local Execution)
`cd deployment/eventPublisher`
`pip install -r requirements.txt`
`python EventPublisher.py`

## 6. Repository Gotchas (Agent Watchlist)
When modifying code or configurations, enforce the following constraints:
- **Duplicated ASN.1 Schemas:** Schemas exist in both `deployment/eventPublisher/asn/` and `deployment/nifi/asn/`. If you modify a schema, **update both locations**.
- **Test Environment Paths:** `test_main_function_with_valid_input` in the NiFi tests resolves `DATA_FOLDER` relative to the test file (`../../asn`). Keep it relative — do not reintroduce machine-specific absolute paths.
- **NiFi Flow Bootstrapping:** The flow is bootstrapped by `nifi-setup` via `nifi-init.sh`, pulling `flow.json` from the Registry. UI edits do not update the committed `flow.json`.
- **Vendored Binaries:** Custom NARs and connector JARs are committed as binaries. Their source code lives in sibling repositories (`instantx-connectors`, `instantx-metrics`).
- **AMQP & Networks:** External AMQP (e.g., RabbitMQ) is wired via NiFi Parameter Context. Connect external brokers to the `deployment_nifi_network` Docker network.
- **Zookeeper vs KRaft:** Kafka runs in KRaft mode. The existing Zookeeper service in `docker-compose` is strictly for NiFi's cluster coordination; do not conflate them.

## 7. Contribution Conventions
- **Workflow:** Fork → feature branch → PR against `main`.
- **Versioning:** Semantic Versioning (SemVer). Record user-facing changes in `CHANGELOG.md` (Keep a Changelog format) and `RELEASE.md`.
- **Standards:** Maintain clean commit histories, strict license headers (First-party code is MIT), and adhere to `CONTRIBUTING.md`.

## 8. Agent Instruction Files (CLAUDE.md ↔ AGENTS.md)
- **Single source of truth:** `AGENTS.md` (this file) is the canonical, committed agent guide. **Do not maintain a separate `CLAUDE.md` with its own content** — it drifts.
- **Why `CLAUDE.md` is git-ignored:** Claude Code looks for `CLAUDE.md`, but committing it would duplicate `AGENTS.md`. `.gitignore` excludes `CLAUDE.md` (and `CLAUDE.local.md`); each developer links it to `AGENTS.md` locally so Claude Code reads the same instructions every other agent uses.
- **One-time setup (run from repo root after cloning):**

  **macOS / Linux:**
  ```bash
  ln -s AGENTS.md CLAUDE.md
  ```

  **Windows — PowerShell** (Developer Mode on, or run as Administrator):
  ```powershell
  New-Item -ItemType SymbolicLink -Path CLAUDE.md -Target AGENTS.md
  ```

  **Windows — cmd.exe** (run as Administrator):
  ```cmd
  mklink CLAUDE.md AGENTS.md
  ```

- **Result:** Edit `AGENTS.md` only; `CLAUDE.md` follows automatically. The symlink is local-only and never committed (it matches the `.gitignore` entry).
- **`CLAUDE.local.md`:** Reserved for per-developer overrides that must never be shared — also git-ignored. Do not put project-wide guidance there.
