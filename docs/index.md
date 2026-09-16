# Introduction

## Rationale

Taking inspiration from the [Contract-First Development](https://openpracticelibrary.com/practice/contract-first-development/) approach, this small tool aims to simplify the development of Python CLI with [Click](https://click.palletsprojects.com/en/stable/) to be integrated in [CWL Command Line Tool](https://www.commonwl.org/user_guide/topics/command-line-tool.html).

Defining the Interface(s) first in the CWL not only speeds up the development, it also alleviates developers to manually write the boilerplate code to implement the CLIs.

## Usage

### Installation

`cwl2click` is published on [Pypi](https://pypi.org/project/cwl2click/), users just have to install it wia `pip`

!!! Release note

    Since release **0.9.0**, `cwl2puml` is a transpiler-mate plugin.
    The standalone command was removed; use `transpiler-mate cwl2puml`.
    The Python library remains available.

```console
pip install transpiler-mate-runtime "cwl2click>=0.9.0"
```
