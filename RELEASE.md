# Releases

InstantX uses [Semantic Versioning](https://semver.org/). The notes below summarize the major changes per version; see [CHANGELOG.md](./CHANGELOG.md) for the detailed log.

## Release process & signature verification

Releases are identified by **signed Git tags**, signed with [Sigstore `gitsign`](https://github.com/sigstore/gitsign) (keyless signing via OIDC — no long-lived keys to manage). To verify a release tag, install `gitsign` and verify the tag, e.g.:

```sh
gitsign verify-tag \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  --certificate-identity-regexp="lf-edge/instantx" \
  <tag>
```

Adjust the `--certificate-identity`/`--certificate-oidc-issuer` to match the maintainer or CI workflow that produced the signature (see the gitsign documentation). The release-manager role is described in [GOVERNANCE.md](./GOVERNANCE.md).

## Upgrade path

Versions follow SemVer: upgrades within the same MAJOR are backward compatible. To upgrade, check out the new tag and rebuild the stack:

```sh
git fetch --tags && git checkout <new-tag>
cd deployment && docker-compose up --build -d
```

Breaking changes (MAJOR bumps) and any required migration steps are called out in the release notes below and in [CHANGELOG.md](./CHANGELOG.md).

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
