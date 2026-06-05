# Contributing to InstantX

First off, thank you for taking the time to contribute! ❤️

The [InstantX] community shares the spirit of the [Apache Way](https://apache.org/theapacheway/) and believes in "Community over Code". We welcome any and all types of contributions that benefit the community at large:

* Star the project
* Refer this project in your project's documentation
* Provide user feedback
* Share your use cases
* Collaborate with related products and technologies
* Maintain our wiki and improve documentation
* Contribute test scenarios and test code
* Fix bugs and add new features

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting a Bug](#reporting-a-bug)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Code Contribution](#code-contribution)
    - [Contribution Process](#contribution-process)
  - [Testing Policy](#testing-policy)
  - [Coding Standards](#coding-standards)
  - [Improving the Documentation](#improving-the-documentation)

## Code of Conduct

This project and everyone participating in it is governed by the [InstantX Code of Conduct](./CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers listed in [MAINTAINERS.md](./MAINTAINERS.md).

## I Want To Contribute

> Looking for help rather than contributing? See [SUPPORT.md](./SUPPORT.md) for the available support channels.

### Reporting a Bug

A great way to contribute to the project is to send a detailed report when you encounter an issue.

#### Before Submitting a Bug Report

- Confirm you are using the latest version.
- Check that your bug is really a bug and not a configuration issue on your side (e.g. using incompatible components/versions, or missing configuration files). Make sure you have read the [deployment instructions](./deployment/Quick-Start.md). If you are looking for support, check [SUPPORT.md](./SUPPORT.md).
- Search [our issue database] to confirm the problem or suggestion has not already been reported.
  - If you find a match, use the "subscribe" button to get notified on updates.
  - Do *not* leave random "+1" or "I have this too" comments — they clutter the discussion without helping to resolve it.
  - If you can reproduce the issue or have additional information that may help resolve it, please leave a comment.
- Search the internet (including [Stack Overflow]) to see if users outside of the GitHub community have discussed the issue.

#### How Do I Submit a Good Bug Report?

We use [GitHub Issues] to track bugs and errors. If you run into an issue with the project:

- Open an [Issue]. (Since we can't be sure at this point whether it is a bug, please don't label the issue as a bug yet.)
- Explain the behavior you expected and the actual behavior.
- Provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue. This usually includes your configuration and, where relevant:
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version(s) of the interpreter / compiler / SDK / runtime environment, depending on what seems relevant.
  - Stack traces (log files). When sending lengthy log files, consider posting them as a [gist](https://gist.github.com).

> Don't forget to remove **sensitive data** from your log files before posting (you can replace those parts with "REDACTED").
>
> You must never report **security-related issues**, vulnerabilities, or bugs containing sensitive information to the issue tracker, or elsewhere in public. Please follow [SECURITY.md](./SECURITY.md) instead.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps.
- If the team is able to reproduce the issue, it will be marked `needs-fix` (and possibly other tags such as `critical`), and left to be implemented by a contributor.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for InstantX, **including completely new features and minor improvements to existing functionality**. Following these guidelines helps maintainers and the community understand your suggestion and find related ones.

#### Before Submitting an Enhancement

- Make sure you are using the latest version.
- Read the [documentation](./README.md) carefully and find out if the functionality is already covered, or included in the [Roadmap](./README.md#roadmap) of future use cases.
  - For a planned roadmap feature, check with the project [Maintainers](./MAINTAINERS.md) to confirm whether it is already in progress, or still in the backlog and therefore available for you to pick up.
- Perform a [search] to see if the enhancement has already been suggested.
  - If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits the scope and aims of the project. It's up to you to make a strong case for the merits of the feature. Keep in mind that we want features useful to the majority of our users. If you're targeting a minority of users, consider writing an add-on/plugin library.

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [Issues].

- Use a **clear and descriptive title** to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as much detail as possible.
- **Describe the current behavior** and **explain which behavior you expected** instead, and why. You can also tell which alternatives do not work for you.
- **Explain why this enhancement would be useful** to InstantX users. You may point out other projects that solved it well and could serve as inspiration.

### Code Contribution

We appreciate your contribution to this project! If you have any questions, feel free to reach out to the [maintainers](./MAINTAINERS.md) through the project's issue tracker.

> #### Legal Notice
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content, and that the content you contribute may be provided under the project [license](./LICENSE.md).

#### Developer Certificate of Origin (DCO)

All contributions must be signed off under the [Developer Certificate of Origin](https://developercertificate.org/). Add a `Signed-off-by` line to every commit by committing with `-s`:

```sh
git commit -s -m "Your message"
```

This certifies that you wrote the change (or otherwise have the right to submit it) under the project license. A CI check enforces the sign-off on every pull request — commits without a `Signed-off-by` line will fail.

> #### Verification
> We may request additional information or verification if there are any concerns regarding the origin or licensing of your code.

#### Contribution Process

1. **Fork the repository** — Create a fork of this repository on your GitHub account.
2. **Create a branch** — Create a branch for your code changes.
3. **Implement your changes** — Make your changes to the codebase, including tests (see [Testing Policy](#testing-policy)).
4. **Commit your changes** — Commit with a clear, descriptive message and sign off with `git commit -s` (see [Developer Certificate of Origin](#developer-certificate-of-origin-dco)).
5. **Push your changes** — Push your changes to your forked branch.
6. **Open a pull request** — Open a pull request from your forked branch to the `main` branch of this repository, filling in the pull request template.
7. **Wait for feedback** — Wait for the team to review your PR and act upon it.

### Testing Policy

Quality is a shared responsibility. To keep the project maintainable:

- **Major new functionality MUST be accompanied by automated tests.** Pull requests that add or change first-party behavior are expected to add or update the corresponding tests.
- Bug fixes SHOULD include a regression test that fails before the fix and passes after it, where practical.
- The pull request template includes a checklist item confirming that tests were added or updated.

The first-party Python test suite lives in [`deployment/nifi/nifi-scripts`](./deployment/nifi/nifi-scripts) and is run with `pytest`. See the [Development guide](./docs/Development.md) for how to run tests, linting, and static analysis locally.

### Coding Standards

To keep contributions consistent and clean:

- Write clean, well-documented code, and include a license header on new first-party source files (first-party code is MIT).
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python; it is enforced automatically by [`ruff`](https://docs.astral.sh/ruff/) (configuration in `deployment/nifi/nifi-scripts/pyproject.toml`).
- Lint with `ruff` and scan with [`bandit`](https://bandit.readthedocs.io/) before opening a PR — see the [Development guide](./docs/Development.md). CI runs both on every PR.
- Follow the existing style and structure of the surrounding code.

### Improving the Documentation

We greatly welcome contributions to our documentation! Help in improving its clarity, accuracy, and completeness is invaluable. There are two main areas:

- **Wiki** — The InstantX project encourages community sharing through its [Wiki]; feel free to add any relevant content.
- **Project documentation** — All documentation that is part of the source repository. It follows the same [Code Contribution](#code-contribution) process above.

> Additional tips:
> - Use clear and concise language.
> - Include examples and code snippets to illustrate concepts.
> - Proofread your work carefully.
> - Consider using diagrams or flowcharts to visualize complex processes.

Thank you for your contributions! Your efforts help make this project more accessible and user-friendly.

[InstantX]: https://github.com/lf-edge/instantx
[search]: https://github.com/lf-edge/instantx/issues
[Issue]: https://github.com/lf-edge/instantx/issues
[Issues]: https://github.com/lf-edge/instantx/issues
[GitHub Issues]: https://github.com/lf-edge/instantx/issues
[Wiki]: https://github.com/lf-edge/instantx/wiki
[our issue database]: https://github.com/lf-edge/instantx/issues
[Stack Overflow]: https://stackoverflow.com/questions/tagged/InstantX
