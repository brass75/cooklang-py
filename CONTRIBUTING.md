# Contributing to `cooklang-py`

This document will help you get started in contributing to the `cooklang-py` codebase.
`cooklang-py` is an open source project and contributions are welcome. Please follow
these guidlines to help you with your contributions.

## LLM Contributions

Contributions that are authored by LLMs, agents, or individuals using LLMs are not welcome in this repository.
If the maintainers have reason to believe that a PR was created with LLM generated code it will be closed
immediately.

The maintainers of this project use the `gh-profiler` tool to assist in determining whether a PR is made by
a human or with LLM generated code.

## Before you Contribute

When suggesting a feature, consider the following:

- `cooklang-py` is a parser for the [Cooklang](https://www.cooklang.org) Recipe Markup
Language. Any functionality implemented must comply with the
[language specification](https://cooklang.org/docs/spec/).
- The goal of `cooklang-py` is to be a Python parse for Cooklang. It is intended to be used
by other tools to allow them to leverage the language. Features that make implementing
tools that use Cooklang easier will be considered for implementation.

## Filing an Issue

> **There is no issue too small to be an issue**

If you see or experience a problem, please file an issue. Include any important informationas it is relevant such as:

- Summary of Actions
- Operating System
- Python Version
- Recipe, metadata, or steps that are at issue.
- Output

## Wait to be Assigned Issues

In order to prevent multiple people from working on the same issue, please wait to be
assigned an issue. If there is an issue that you are interested in working on please add a
comment to that effect and a maintainer will assign it to you if it is not being worked.

## Checking out the codebase

Please be sure to fork the repo before submitting pull requests. Pull requests from branches
of the repo are only permitted for maintainers.

## Setup your Environment

The `cooklang-py` uses `uv` as both its dependency management and build system.
To setup a working environment, run:

```
uv sync -p 3.10
```

Please always use the oldest supported Python version (currently 3.10) for your
development environment.

## Verify Before Submitting

PRs will not be approved without tests passing on all supported versions.

- 🚫 changes aren't breaking existing code (failing tests)
- 🚫 Ensure new dependencies are listed, justified, and approved to be added.

To test please use the oldest and newest supported Python version (currently 3.10 and 3.13)
to ensure full compatibility:

```
uv run -p 3.10 pytest tests
uv run -p 3.13 pytest tests
```

## Formatting your PR

Please be sure to include the following:

- Summary
- issue(s)/discussions being addressed
- Documentation or tests added/updated
- Any follow up tasks pending
