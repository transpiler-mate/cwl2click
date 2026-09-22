# Execution

Based on a KISS approach:

```bash
Usage: transpiler-mate cwl2click [OPTIONS] SOURCE

  Boostrap a Python CLI using click from a CWL CommandLineTool(s).

Options:
  --oci-hostname TEXT   [env var: OCI_HOSTNAME]
  --oci-username TEXT   [env var: OCI_USERNAME]
  --oci-password TEXT   [env var: OCI_PASSWORD]
  --oauth2-bearer TEXT  [env var: OAUTH2_BEARER]
  --bundle              Bundle all tools into one module with subcommands
  --clt-id TEXT         ID(s) of the CommandLineTools
  --output PATH         Output directory path  [required]
  --help                Show this message and exit.
```

Users can generate `Click` code by executing:

```bash
$ transpiler-mate cwl2click --bundle \
    --output ./src/test \
    https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl
```

and monitor the execution:

```log
2026-09-16 12:16:39.840 | INFO     | transpiler_mate.runtime.cli:invoke_plugin:280 - 
━┏┛┏━┃┏━┃┏━ ┏━┛┏━┃┛┃  ┏━┛┏━┃  ┏┏ ┏━┃━┏┛┏━┛
 ┃ ┏┏┛┏━┃┃ ┃━━┃┏━┛┃┃  ┏━┛┏┏┛  ┃┃┃┏━┃ ┃ ┏━┛
 ┛ ┛ ┛┛ ┛┛ ┛━━┛┛  ┛━━┛━━┛┛ ┛  ┛┛┛┛ ┛ ┛ ━━┛

 v1.0.1 by Terradue srl
 info[at]terradue[dot]com

2026-09-16 12:16:39.840 | INFO     | transpiler_mate.runtime.cli:invoke_plugin:289 - Started at: 2026-09-16T12:16:39.840
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:68 - Mounting 'http://' scheme to 'HTTPAdapter'...
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:70 - Scheme 'http://' successfully mount to 'HTTPAdapter'
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:68 - Mounting 'https://' scheme to 'HTTPAdapter'...
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:70 - Scheme 'https://' successfully mount to 'HTTPAdapter'
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:68 - Mounting 'file://' scheme to 'FileAdapter'...
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:70 - Scheme 'file://' successfully mount to 'FileAdapter'
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:68 - Mounting 'oci://' scheme to 'OCIAdapter'...
2026-09-16 12:16:39.841 | DEBUG    | transpiler_mate.runtime.context_resolver:_mount_session:70 - Scheme 'oci://' successfully mount to 'OCIAdapter'
2026-09-16 12:16:39.841 | DEBUG    | cwl_loader:load_cwl_from_location:368 - Loading CWL document from https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl...
2026-09-16 12:16:40.043 | DEBUG    | cwl_loader:_load_cwl_from_stream:371 - Reading stream from https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl...
2026-09-16 12:16:40.077 | DEBUG    | cwl_loader:load_cwl_from_stream:338 - CWL data of type <class 'ruamel.yaml.comments.CommentedMap'> successfully loaded from stream
2026-09-16 12:16:40.077 | DEBUG    | cwl_loader:load_cwl_from_yaml:261 - No needs to update the Raw CWL document since it targets already the v1.2
2026-09-16 12:16:40.077 | DEBUG    | cwl_loader:load_cwl_from_yaml:265 - Parsing the raw CWL document to the CWL Utils DOM...
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:load_cwl_from_yaml:274 - Raw CWL document successfully parsed to the CWL Utils DOM!
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:load_cwl_from_yaml:276 - Dereferencing the steps[].run...
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader._dereference:_dereference_step:143 - Checking if https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl#crop must be externally imported...
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader._dereference:_dereference_step:145 - run_url: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl - uri: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader._dereference:_dereference_step:143 - Checking if https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl#norm_diff must be externally imported...
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader._dereference:_dereference_step:145 - run_url: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl - uri: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader._dereference:_dereference_step:143 - Checking if https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl#otsu must be externally imported...
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader._dereference:_dereference_step:145 - run_url: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl - uri: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:load_cwl_from_yaml:285 - steps[].run successfully dereferenced! Dereferencing the FQNs...
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:load_cwl_from_yaml:289 - CWL document successfully dereferenced! Now verifying steps[].run integrity...
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:load_cwl_from_yaml:295 - All steps[].run link are resolvable! 
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:load_cwl_from_yaml:298 - Sorting Process instances by dependencies....
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:load_cwl_from_yaml:300 - Sorting process is over.
2026-09-16 12:16:48.834 | DEBUG    | cwl_loader:_load_cwl_from_stream:381 - Stream from https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl successfully load!
2026-09-16 12:16:48.848 | DEBUG    | cwl2click:to_click_type:159 - Type <cwl_utils.parser.cwl_v1_2.CommandInputArraySchema object at 0x7250ef1094b0>, represented by key type Directory, mapped to Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True)
2026-09-16 12:16:48.848 | DEBUG    | cwl2click:is_required:76 - Detected type <cwl_utils.parser.cwl_v1_2.CommandInputArraySchema object at 0x7250ef1094b0> as required: True
2026-09-16 12:16:48.848 | DEBUG    | cwl2click:to_click_type:159 - Type Directory, represented by key type Directory, mapped to Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True)
2026-09-16 12:16:48.849 | DEBUG    | cwl2click:is_required:76 - Detected type Directory as required: True
2026-09-16 12:16:48.849 | DEBUG    | cwl2click:to_click_type:159 - Type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI, represented by key type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI, mapped to STRING
2026-09-16 12:16:48.849 | DEBUG    | cwl2click:is_required:76 - Detected type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI as required: True
2026-09-16 12:16:48.849 | DEBUG    | cwl2click:to_click_type:159 - Type Directory, represented by key type Directory, mapped to Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True)
2026-09-16 12:16:48.849 | DEBUG    | cwl2click:is_required:76 - Detected type Directory as required: True
2026-09-16 12:16:48.849 | DEBUG    | cwl2click:to_click_type:159 - Type Directory, represented by key type Directory, mapped to Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True)
2026-09-16 12:16:48.849 | DEBUG    | cwl2click:is_required:76 - Detected type Directory as required: True
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:to_click_type:159 - Type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI, represented by key type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI, mapped to STRING
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:is_required:76 - Detected type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI as required: True
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:to_click_type:159 - Type Directory, represented by key type Directory, mapped to Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True)
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:is_required:76 - Detected type Directory as required: True
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:to_click_type:159 - Type https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox, represented by key type https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox, mapped to STRING
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:is_required:76 - Detected type https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox as required: True
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:to_click_type:159 - Type https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox, represented by key type https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox, mapped to STRING
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:is_required:76 - Detected type https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox as required: True
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:to_click_type:159 - Type string, represented by key type string, mapped to STRING
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:is_required:76 - Detected type string as required: True
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:to_click_type:159 - Type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI, represented by key type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI, mapped to STRING
2026-09-16 12:16:48.850 | DEBUG    | cwl2click:is_required:76 - Detected type https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI as required: True
2026-09-16 12:16:48.850 | SUCCESS  | cwl2click.plugin:cwl2click:73 - 'https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop/cwl-workflow/pattern-12.cwl' successfully converted to Click Python application in '/home/stripodi/Downloads/src/test/pattern_12.py'.
2026-09-16 12:16:48.850 | SUCCESS  | transpiler_mate.runtime.cli:invoke_plugin:326 - ------------------------------------------------------------------------
2026-09-16 12:16:48.850 | SUCCESS  | transpiler_mate.runtime.cli:invoke_plugin:327 - SUCCESS
2026-09-16 12:16:48.850 | SUCCESS  | transpiler_mate.runtime.cli:invoke_plugin:328 - ------------------------------------------------------------------------
2026-09-16 12:16:48.850 | INFO     | transpiler_mate.runtime.cli:invoke_plugin:331 - Total time: 9.0096 seconds
2026-09-16 12:16:48.850 | INFO     | transpiler_mate.runtime.cli:invoke_plugin:332 - Finished at: 2026-09-16T12:16:48.850
```

As reported in the `SUCCESS` logging message, the `Click` application is serialized to the `/path/to/your-project/src/your-module/pattern-12.py` file:

```pyton
# File generated by cwl2click v0.8.0
# timestamp: 2026-09-16T12:16:48.848

__all__ = []

from test.norm_diff_impl import execute as norm_diff_command
from test.otsu_impl import execute as otsu_command
from test.crop_impl import execute as crop_command

from pathlib import Path

import click







# None
__all__.append("runner")
# NOTE
# Do not forget to add the section below in your `pyproject.toml` file
#  
# [project.scripts]
# ndi-cli = "test.norm_diff:runner"
@click.group()
def runner() -> None:
    pass



runner.add_command(
    click.Command(
        name="ndi-cli",
        callback=norm_diff_command,
        help="""No info provided""",
        short_help="""No info provided""",
        params=[
            click.Option(
                ["--rasters"],
                "rasters",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=True,
                required=True,
                is_flag=False,
            ),
            click.Option(
                ["--item"],
                "item",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=False,
                required=True,
                is_flag=False,
            ),
            click.Option(
                ["--collection"],
                "collection",
                type=click.STRING,
                multiple=False,
                required=True,
                is_flag=False,
            ),
        ]
    )
)








runner.add_command(
    click.Command(
        name="otsu-cli",
        callback=otsu_command,
        help="""No info provided""",
        short_help="""No info provided""",
        params=[
            click.Option(
                ["--input-ndi"],
                "raster",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=False,
                required=True,
                is_flag=False,
            ),
            click.Option(
                ["--item"],
                "item",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=False,
                required=True,
                is_flag=False,
            ),
            click.Option(
                ["--collection"],
                "collection",
                type=click.STRING,
                multiple=False,
                required=True,
                is_flag=False,
            ),
        ]
    )
)








runner.add_command(
    click.Command(
        name="crop-cli",
        callback=crop_command,
        help="""No info provided""",
        short_help="""No info provided""",
        params=[
            click.Option(
                ["--input-item"],
                "item",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=False,
                required=True,
                is_flag=False,
            ),
            click.Option(
                ["--aoi"],
                "aoi",
                type=click.STRING,
                multiple=False,
                required=True,
                is_flag=False,
                help="""Area of interest defined as a bounding box""",
            ),
            click.Option(
                ["--epsg"],
                "epsg",
                type=click.STRING,
                multiple=False,
                required=True,
                is_flag=False,
            ),
            click.Option(
                ["--band"],
                "band",
                type=click.STRING,
                multiple=False,
                required=True,
                is_flag=False,
            ),
            click.Option(
                ["--collection"],
                "collection",
                type=click.STRING,
                multiple=False,
                required=True,
                is_flag=False,
            ),
        ]
    )
)
```
