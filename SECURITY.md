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

## Response Time

We will acknowledge your report and provide an initial response **within 14 days** of receiving it. We will keep you informed of the progress towards a fix and may ask for additional information or guidance. Once a fix is available, we will coordinate the disclosure timeline with you.

## Cryptography

InstantX first-party code does **not** implement its own cryptographic algorithms or protocols. The platform's payload handling (UPER / ASN.1 encoding of ETSI C-ITS messages) is **not** cryptography. Confidentiality and integrity in transit are provided by the underlying, configurable infrastructure (TLS for MQTT, Kafka, and HTTP endpoints) using the standard implementations shipped with those components. Operators are responsible for enabling TLS and managing keys/certificates for their deployment.

## Supported Versions

Security fixes are applied to the latest released version. Please ensure you are running the most recent release before reporting an issue. Publicly known, fixed run-time vulnerabilities (if any) are recorded in [CHANGELOG.md](./CHANGELOG.md).
