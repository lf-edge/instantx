# Security Policy

## Reporting Security Issues

If you believe you have found a security vulnerability in any **InstantX** component, please report it to us through coordinated disclosure.

**Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.**

Instead, please send an email to **instantxsupport@vodafone.com**.

Please include as much of the information listed below as you can to help us better understand and resolve the issue:

  * The type of issue (e.g., buffer overflow, SQL injection, or cross-site scripting)
  * Full paths of source file(s) related to the manifestation of the issue
  * The location of the affected source code (tag/branch/commit or direct URL)
  * Any special configuration required to reproduce the issue
  * Step-by-step instructions to reproduce the issue
  * Proof-of-concept or exploit code (if possible)
  * Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Disclosure and Response Process

We follow coordinated disclosure:

1. **Acknowledge** — we provide an initial response **within 14 days** of receiving your report.
2. **Triage** — we confirm the issue, assess severity (CVSS), and identify the affected versions.
3. **Fix** — we develop and test a fix, using a private branch when necessary to avoid premature disclosure.
4. **Release & disclose** — we release the fix, record it in [CHANGELOG.md](./CHANGELOG.md), and coordinate public disclosure (and CVE assignment, where applicable) with you. We aim to fix and disclose medium-or-higher severity issues within 90 days of triage.

We will keep you informed of progress throughout and may ask for additional information or guidance.

## Credit

Unless you request otherwise (including a request to remain anonymous), we credit reporters of valid vulnerabilities in the release notes or advisory that accompanies the fix.

## Cryptography

InstantX first-party code does **not** implement its own cryptographic algorithms or protocols. The platform's payload handling (UPER / ASN.1 encoding of ETSI C-ITS messages) is **not** cryptography. Confidentiality and integrity in transit are provided by the underlying, configurable infrastructure (TLS for MQTT, Kafka, and HTTP endpoints) using the standard implementations shipped with those components. Operators are responsible for enabling TLS and managing keys/certificates for their deployment.

## Supported Versions

Security fixes are applied to the latest released version. Please ensure you are running the most recent release before reporting an issue. Publicly known, fixed run-time vulnerabilities (if any) are recorded in [CHANGELOG.md](./CHANGELOG.md).

## Security Architecture & Threat Model

For the project's security requirements, secure-design principles, hardening guidance, and threat model, see [docs/Security-Architecture.md](./docs/Security-Architecture.md) and [docs/Threat-Model.md](./docs/Threat-Model.md).
