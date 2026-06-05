# InstantX Governance

This document describes how the InstantX project is governed: how decisions are
made, the roles involved, and how the project continues operating over time. It
complements [MAINTAINERS.md](./MAINTAINERS.md) (who the maintainers are) and
[CONTRIBUTING.md](./CONTRIBUTING.md) (how to contribute).

## Project model

InstantX is an open-source project hosted under the [LF Edge](https://www.lfedge.org/)
umbrella and developed primarily by Vodafone Business. It follows a **maintainer-led**
("do-ocracy") model in the spirit of the [Apache Way](https://apache.org/theapacheway/):
those who do the work and earn the community's trust make the decisions, in the open.

The project adheres to the [LF Edge Code of Conduct](./CODE_OF_CONDUCT.md).

## Roles and responsibilities

| Role | Who | Responsibilities |
|------|-----|------------------|
| **Contributor** | Anyone | Opens issues, proposes changes via pull requests, improves docs/tests. |
| **Maintainer** | Listed in [MAINTAINERS.md](./MAINTAINERS.md) | Reviews and merges pull requests, triages issues, sets technical direction, cuts releases. |
| **Security responder** | Maintainers | Receives private vulnerability reports (see [SECURITY.md](./SECURITY.md)), coordinates triage, fix, and disclosure. |
| **Release manager** | A maintainer (rotating) | Tags and signs releases, updates `CHANGELOG.md` / `RELEASE.md`. |

## Decision-making

- **Routine changes** (bug fixes, docs, tests, dependency bumps) are decided by
  **lazy consensus**: a maintainer reviews and approves the pull request. Any
  maintainer may request changes.
- **Significant changes** (architecture, new components, breaking changes) are
  proposed in a GitHub issue or pull request and discussed openly. Consensus
  among the active maintainers is sought; if consensus cannot be reached, a
  simple majority of active maintainers decides.
- All decisions happen in the open on the [issue tracker](https://github.com/lf-edge/instantx/issues)
  and pull requests, so they are searchable and auditable.

## Becoming a maintainer

Contributors who have made sustained, high-quality contributions (code, reviews,
documentation, or community support) over time may be nominated as maintainers by
an existing maintainer. Nominations are approved by consensus of the current
maintainers and recorded by adding the person to [MAINTAINERS.md](./MAINTAINERS.md).

## Access continuity

To ensure the project can continue if any single person becomes unavailable:

- The repository lives in the **`lf-edge` GitHub organization**, administered by
  the Linux Foundation; org owners can restore access independently of any
  individual maintainer.
- There are **multiple active maintainers** (see [MAINTAINERS.md](./MAINTAINERS.md)),
  so more than one person can review, merge, and release.
- Releases and CI run from configuration committed to the repository
  (`.github/workflows/`), not from any individual's machine.

If a maintainer is unreachable for an extended period, the remaining maintainers
continue normal operations; routine work is not blocked on any one person.

## Changing this document

Changes to governance are themselves "significant changes" and follow the
decision-making process above.
