# cwl2click

Boostrap a Python CLI using `click` from a CWL `CommandLineTool`(s).

[![PyPI - Version](https://img.shields.io/pypi/v/cwl2click.svg)](https://pypi.org/project/cwl2click)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cwl2click.svg)](https://pypi.org/project/cwl2click)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/transpiler-mate/cwl2click/package.yaml?branch=develop&event=push&label=build&logo=githubactions)](https://github.com/transpiler-mate/cwl2click/actions/workflows/package.yaml?query=branch%3Adevelop)
[![Code coverage](https://img.shields.io/codecov/c/github/transpiler-mate/cwl2click/develop?logo=codecov)](https://app.codecov.io/gh/transpiler-mate/cwl2click/tree/develop)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

> [!NOTE]
> Since release **0.9.0**, `cwl2puml` is a transpiler-mate plugin.
> The standalone command was removed; use `transpiler-mate cwl2puml`.
> The Python library remains available.

```console
pip install transpiler-mate-runtime "cwl2click>=0.9.0"
```

### Local quality checks

Install [Hatch](https://hatch.pypa.io/) and [Taskfiles](https://taskfile.dev/docs/guide) then install the Git hook:

```console
task quality:pre-commit:install
```

Every commit runs Ruff (including the configured McCabe complexity limit),
Ruff formatting, strict mypy checks, and the pytest suite.
Run the complete hook explicitly with:

```console
task quality:pre-commit:run

## License

[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
