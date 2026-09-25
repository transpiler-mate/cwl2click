import sys
from unittest import TestCase

import click
from click.testing import CliRunner
from cwl_utils.parser import cwl_v1_0, cwl_v1_1, cwl_v1_2

from cwl2click import to_snake_case
from cwl2click.plugin import Cwl2ClickOptions, cwl2click
from tests.utils import CWLClickTestCase


class TestStandalone(CWLClickTestCase, TestCase):
    def test_default_generates_separate_direct_commands(self) -> None:
        context = self.create_context("tests/data/multiple-basecommands.cwl")
        # Shared base commands must remain independent, and IDs retain their
        # original spelling in the project directory only.
        document = dict(context.document)
        tool = document.pop("clt_id_2")
        assert isinstance(
            tool, (cwl_v1_0.CommandLineTool, cwl_v1_1.CommandLineTool, cwl_v1_2.CommandLineTool)
        )
        tool.id = "second-tool"
        tool.baseCommand = ["basecommand", "second"]
        document[tool.id] = tool
        context = context.model_copy(update={"document": document})
        cwl2click.execute(context, Cwl2ClickOptions(output=self.tmp_path))

        self.assertEqual(len(list(self.tmp_path.rglob("cli.py"))), 4)
        self.assertEqual(list(self.tmp_path.glob("*.py")), [])
        for tool_id in ["clt_id", "second-tool"]:
            package = to_snake_case(tool_id)
            source_dir = self.tmp_path / tool_id / "src"
            cli_path = source_dir / package / "cli.py"
            self.assertTrue(cli_path.is_file())
            impl = source_dir / package / f"{package}_impl.py"
            impl.write_text("def execute(input):\n    print(input)\n")
            sys.path.insert(0, str(source_dir))
            self._added_sys_paths.append(str(source_dir))
            self._imported_modules.extend([package, f"{package}.{package}_impl"])
            cli = self._import_cli(cli_path)
            self.assertIsInstance(cli, click.Command)
            self.assertNotIsInstance(cli, click.Group)
            result = CliRunner().invoke(cli, ["--input", "value"])
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertEqual(result.output, "value\n")
            result = CliRunner().invoke(cli, ["--help"])
            self.assertIn("--input TEXT", result.output)
            self.assertIn("this is doc", result.output)
            self.assertIn(f"{package}.cli:basecommand", cli_path.read_text())

    def test_selection_applies_before_standalone_generation(self) -> None:
        context = self.create_context("tests/data/multiple-basecommands.cwl")
        cwl2click.execute(context, Cwl2ClickOptions(output=self.tmp_path, clt_id=["clt_id"]))
        self.assertEqual(
            list(self.tmp_path.rglob("*.py")),
            [self.tmp_path / "clt_id" / "src" / "clt_id" / "cli.py"],
        )
