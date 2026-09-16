# Using the transpiler-mate plugin

!!! note "Available since cwl2click 0.9.0"

    Since **0.9.0**, command-line conversion is provided by
    `transpiler-mate cwl2click`. The standalone `cwl2click` command was removed.
    The Python library remains available independently of the runtime.

The plugin bootstraps a Python CLI using Click from CWL `CommandLineTool`
definitions. It generates command definitions and input options, with imports
for callback functions that you implement separately. It does not execute the
CWL tools or generate their processing logic.

## Installation

Install the runtime and plugin in the same Python environment (Python 3.10 or
later):

```bash
pip install transpiler-mate-runtime "cwl2click>=0.9.0"
```

The plugin depends on `transpiler-mate-api`. The separate
`transpiler-mate-runtime` package provides the command and discovers installed
plugins automatically.

```bash
transpiler-mate --help
transpiler-mate cwl2click --help
```

Your generated application also needs `click` as a dependency.

## Convert a CWL document

Generate a Python module from all CommandLineTools available in the resolved
document:

```bash
transpiler-mate cwl2click --output ./src/my_app application.cwl
```

Select specific tools by repeating `--clt-id`:

```bash
transpiler-mate cwl2click \
  --clt-id crop \
  --clt-id norm_diff \
  --output ./src/my_app \
  application.cwl
```

Use the tool IDs in the resolved document. The runtime loads the source and
supplies the context; the plugin requests `CommandLineTool` processes, optionally
filtered by these IDs. Workflows themselves are not converted into commands.

## Options

| Option | Default | Description |
| --- | --- | --- |
| `--clt-id TEXT` | All CommandLineTools | Repeat to select multiple tool IDs. |
| `--output PATH` | Required; no default | Directory in which to write the generated Python module. |

Source loading and application metadata validation are handled by the runtime.
See `transpiler-mate cwl2click --help` for shared authentication options and
[Execution](execution.md) for a remote-source example.

## Generated output

The plugin writes one Python file directly into the output directory, containing
all selected tools. The filename comes from the source URL or path's filename,
with its extension replaced by `.py` and its stem converted to snake case.
For example, `pattern-12.cwl` produces:

```text
src/
└── my_app/
    └── pattern_12.py
```

Missing directories are created. An existing file with the same name is
overwritten, and other files are retained. Generation errors are reported as
`PluginExecutionError`; because the target is opened before rendering, a failure
can leave an empty or incomplete output file.

The generated module uses the output directory's final name (`my_app` above) as
the package name in callback imports. Choose an output directory whose name is
a valid Python package name and make that package importable in your application.

For a tool with ID `crop`, the generated import is:

```python
from my_app.crop_impl import execute as crop_command
```

Create `my_app/crop_impl.py` yourself and provide an `execute` function accepting
the generated input names as keyword arguments. Tool IDs and callback parameter
names are converted to snake case. The plugin does not create implementation
modules, `__init__.py`, or project packaging files.

## Command structure and application setup

Each selected tool must define `baseCommand`. Its first item (or the whole value
when it is a string) determines the generated command or group variable, converted
to snake case. A second `baseCommand` item supplies a subcommand name; otherwise,
the first `arguments` item is used when present. Tools with subcommands and the
same base command share a Click group.

Inputs become Click options using `inputBinding.prefix`, or `--<input-id>` when
no prefix is supplied. CWL types determine the Click types, required status,
repeatable options, and boolean flags. Tool labels and documentation supply help
text. See the [crosswalk](crosswalk.md) for mapping details.

To expose the generated CLI, add a script entry point to your application's
`pyproject.toml`. For example, if `application.cwl` defines a tool with
`baseCommand: runner` and you generated `src/my_app/application.py`, use:

```toml
[project.scripts]
my-cli = "my_app.application:runner"
```

Use the actual generated module filename and command or group variable in this
entry point. The generated comments contain entry-point suggestions based on
tool IDs, which can differ from the source-based module filename.

After providing the callback implementations, declaring the `click` dependency,
and installing your application, inspect its commands with:

```bash
my-cli --help
```

## Migrating from the former CLI

Install the runtime alongside the plugin and replace `cwl2click` with
`transpiler-mate cwl2click`. Supply the required `--output` directory and use
repeated `--clt-id` options to restrict generation to particular tools.

## Plugin registration

The package declares this entry point:

```toml
[project.entry-points."transpiler_mate.plugins"]
cwl2click = "cwl2click.plugin:cwl2click"
```

The plugin validates options with `Cwl2ClickOptions` and receives a
`TranspilerContext` from the runtime. Unknown option fields are rejected.
See the [API reference](api.md) for the registration and options model, and for
the `to_click` function if you want to render to a stream directly.
