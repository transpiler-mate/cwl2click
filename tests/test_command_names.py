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

import pytest
from cwl_utils.parser.cwl_v1_2 import CommandLineBinding, CommandLineTool

from cwl2click import get_base_command, get_command_name


@pytest.mark.parametrize("base_command", ["tool", ["tool"], ["tool", "subcommand"]])
def test_base_command_uses_executable(base_command: str | list[str]) -> None:
    tool = CommandLineTool(inputs=[], outputs=[], baseCommand=base_command)
    assert get_base_command(tool) == "tool"


@pytest.mark.parametrize("base_command", [None, [], [42]])
def test_base_command_rejects_missing_or_non_string_names(
    base_command: list[int] | None,
) -> None:
    tool = CommandLineTool(inputs=[], outputs=[], baseCommand=base_command)
    with pytest.raises(ValueError, match="baseCommand"):
        get_base_command(tool)


def test_subcommand_prefers_base_command_over_arguments() -> None:
    tool = CommandLineTool(
        inputs=[], outputs=[], baseCommand=["tool", "subcommand"], arguments=["argument"]
    )
    assert get_command_name(tool) == "subcommand"


def test_argument_binding_is_not_a_subcommand_name() -> None:
    tool = CommandLineTool(
        inputs=[], outputs=[], baseCommand="tool", arguments=[CommandLineBinding(valueFrom="value")]
    )
    assert get_command_name(tool) is None
