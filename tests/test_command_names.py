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
