# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Built-in plugin that serializes the resolved CWL document."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from cwl_utils.parser import CommandLineTool
from loguru import logger
from pydantic import AnyUrl, BaseModel, ConfigDict, Field
from transpiler_mate.api import PluginExecutionError, transpiler_plugin

from . import to_click, to_snake_case

if TYPE_CHECKING:
    from transpiler_mate.api import TranspilerContext


class Cwl2ClickOptions(BaseModel):
    """Options accepted by the cwl2click plugin."""

    model_config = ConfigDict(extra="forbid")

    clt_id: list[str] = Field(
        default_factory=list, description="ID(s) of the CommandLineTools"
    )

    output: Path = Field(description="Output directory path")
    bundle: bool = Field(
        default=False, description="Bundle all tools into one module with subcommands"
    )


def _get_target(workflow: AnyUrl, output: Path) -> Path:
    file_name = Path(workflow.path).name if workflow.path else "UNDEF"  # TODO

    return output / f"{to_snake_case(Path(file_name).stem)}.py"


@transpiler_plugin(
    name="cwl2click",
    description="Boostrap a Python CLI using click from a CWL CommandLineTool(s).",
    options_model=Cwl2ClickOptions,
)
def cwl2click(context: TranspilerContext, options: Cwl2ClickOptions) -> None:
    """Serialize the resolved CWL document to ``options.output``."""

    try:
        command_line_tools = list(
            context.get_processes_by_type(
                CommandLineTool, options.clt_id if options.clt_id else None
            )
        )
        if options.bundle:
            targets = [
                (_get_target(context.source, options.output), command_line_tools)
            ]
        else:
            targets = [
                (
                    options.output / clt.id / "src" / to_snake_case(clt.id) / "cli.py",
                    [clt],
                )
                for clt in command_line_tools
            ]

        for target, tools in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("w") as stream:
                to_click(
                    command_line_tools=tools,
                    module_name=target.parent.absolute().name,
                    output_stream=stream,
                    bundle=options.bundle,
                )

            logger.success(
                f"'{context.source}' successfully converted to Click Python application in "
                f"'{target.absolute()}'."
            )
    except Exception as error:
        raise PluginExecutionError(
            f"An unexpected error occurred while generating CommandLineTool(s) found in input {context.source} CWL document"
        ) from error
