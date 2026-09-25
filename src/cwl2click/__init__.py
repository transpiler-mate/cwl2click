# Copyright 2025 Terradue
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

"""Render Click commands from parsed CWL tools."""

import re
import time
from collections.abc import Iterable, Mapping
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from typing import Any, TextIO

from cwl_utils.parser import CommandLineTool, Process
from jinja2 import Environment, PackageLoader, select_autoescape
from loguru import logger

pattern = re.compile(r"(?<!^)(?=[A-Z])")


def clean_rn(value: str | None) -> str:
    if value:
        paragraphs = [
            " ".join(paragraph.split())
            for paragraph in re.split(r"\n\s*\n", value.strip())
            if paragraph.strip()
        ]
        if paragraphs:
            return "\n\n".join(paragraphs)
    return "No info provided"


def to_triple_quoted_string(value: str | None) -> str:
    text = clean_rn(value)
    escaped = text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return f'"""{escaped}"""'


def to_snake_case(name: str) -> str:
    return pattern.sub("_", name.replace("-", "_")).lower()


def is_array(type_: Any) -> bool:
    return (
        isinstance(type_, list)
        or hasattr(type_, "items")
        or (hasattr(type_, "class_") and type_.class_ == "array")
    )


def _get_array_size(type_: Any) -> int:
    if isinstance(type_, list):
        return len(type_)

    if hasattr(type_, "items"):
        return _get_array_size(type_.items)

    return 0


def is_nullable(type_: Any) -> bool:
    return isinstance(type_, list) and "null" in type_


def is_required(type_: Any) -> bool:
    required: bool = not is_nullable(type_)

    logger.debug(f"Detected type {type_} as required: {required}")

    return required


def is_multiple(type_: Any) -> bool:
    """Indicate whether a CWL input accepts multiple values."""
    if not is_array(type_):
        return False

    array_size = _get_array_size(type_)
    nullable_union_size = 2

    return not (array_size == nullable_union_size and is_nullable(type_))


def is_flag(type_: Any) -> bool:
    """Indicate whether a CWL type includes a boolean flag."""
    return (isinstance(type_, list) and "boolean" in type_) or type_ == "boolean"


def get_base_command(clt: CommandLineTool) -> str:
    """Return the executable name from a CWL tool.

    Raises:
        ValueError: If the tool does not define a string base command.
    """
    if clt.baseCommand:
        if isinstance(clt.baseCommand, list) and len(clt.baseCommand) > 0:
            command = clt.baseCommand[0]
            if isinstance(command, str):
                return command

        if isinstance(clt.baseCommand, str):
            return clt.baseCommand

    raise ValueError(
        f"CommandLineTool '{clt.id}' does not define a 'baseCommand' property, impossible to map it to a `click.Command`"
    )


def get_command_name(clt: CommandLineTool) -> str | None:
    """Return the subcommand name, or None when no string name is defined."""
    if clt.baseCommand:
        if isinstance(clt.baseCommand, list) and len(clt.baseCommand) > 1:
            command = clt.baseCommand[1]
            if isinstance(command, str):
                return command

        if clt.arguments:
            if isinstance(clt.arguments, list):
                command = clt.arguments[0]
                if isinstance(command, str):
                    return command
                return None
            return str(clt.arguments)

    return None


_STRING_FORMAT_SCHEMA_: str = (
    "https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml"
)

_CWL_CLICK_MAP_: Mapping[Any, str] = {
    "int": "INT",
    "long": "INT",
    "double": "FLOAT",
    "float": "FLOAT",
    "boolean": "BOOL",
    "string": "STRING",
    "Directory": "Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True)",
    "File": "Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=True, dir_okay=False)",
    f"{_STRING_FORMAT_SCHEMA_}#DateTime": "DateTime(formats=['%Y-%m-%dT%H:%M:%SZ'])",
    f"{_STRING_FORMAT_SCHEMA_}#UUID": "UUID",
}


def to_click_type(type_: object) -> str:
    """Map a parsed CWL type to a Click parameter type expression."""
    key: object = None

    if isinstance(type_, str):
        key = type_
    elif isinstance(type_, list):
        key = next(item_type for item_type in type_ if item_type != "null")
    elif hasattr(type_, "items"):
        key = type_.items
    elif hasattr(type_, "class_"):
        key = type_.class_
    elif hasattr(type_, "symbols"):
        return f"Choice({[symbol.split('/')[-1] for symbol in type_.symbols]})"

    if key and not isinstance(key, str) and hasattr(key, "symbols"):
        return f"Choice({[symbol.split('/')[-1] for symbol in key.symbols]})"

    mapped_type: str = _CWL_CLICK_MAP_.get(key, "STRING")

    logger.debug(f"Type {type_}, represented by key type {key}, mapped to {mapped_type}")

    return mapped_type


_CWL_PYTHON_MAP_: Mapping[Any, str] = {
    "int": "int",
    "long": "int",
    "double": "float",
    "float": "float",
    "boolean": "bool",
    "string": "str",
    "Directory": "str",
    "File": "str",
}


def to_python_type(type_: object) -> str:
    """Map a parsed CWL type to its Python type name."""
    logger.debug(f"Converting {type_} CWL type to the related Python type...")

    key: object
    if isinstance(type_, str):
        key = type_
    elif isinstance(type_, list):
        key = next(item_type for item_type in type_ if item_type != "null")
    elif hasattr(type_, "class_"):
        key = type_.class_

        if key == "enum":
            key = "string"

    else:
        return str(type_)

    return _CWL_PYTHON_MAP_.get(key, str(type_))


def _to_mapping(functions: list[Any]) -> Mapping[str, Any]:
    mapping: dict[str, Any] = {}

    for function in functions:
        mapping[function.__name__] = function

    return mapping


def _get_version() -> str:
    try:
        return version("cwl2click")
    except PackageNotFoundError:
        return "N/A"


_jinja_environment = Environment(
    loader=PackageLoader(package_name="cwl2click"),
    autoescape=select_autoescape(),
)
_jinja_environment.filters.update(
    _to_mapping(
        [
            clean_rn,
            get_base_command,
            get_command_name,
            is_array,
            is_flag,
            is_multiple,
            is_required,
            is_nullable,
            to_click_type,
            to_python_type,
            to_triple_quoted_string,
            to_snake_case,
        ]
    )
)
_jinja_environment.tests.update(_to_mapping([is_array]))


def to_click(
    command_line_tools: Iterable[Process],
    module_name: str,
    output_stream: TextIO,
    bundle: bool = True,
) -> None:
    """Write generated Click command source to the supplied output stream."""
    template = _jinja_environment.get_template("command_line_tools.py.jinja")

    output_stream.write(
        template.render(
            version=_get_version(),
            timestamp=datetime.fromtimestamp(time.time()).isoformat(timespec="milliseconds"),
            bundle=bundle,
            module_name=module_name,
            command_line_tools=command_line_tools,
        )
    )
