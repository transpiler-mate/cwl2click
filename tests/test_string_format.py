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

from unittest import TestCase

import click
from click import Group

from tests.utils import CWLClickTestCase


class TestStringFormat(CWLClickTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        cli = self.generate_cli("tests/data/string-format.cwl")
        assert isinstance(cli, Group)
        self.cli = cli

    def test_uri_inputs(self) -> None:
        self.assertIn("argument", self.cli.commands)

        cmd = self.cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        self.assertIn("uri_input", params)

        opt = params["uri_input"]

        self.assertEqual(opt.type.name, "text")

    def test_datetime_inputs(self) -> None:
        self.assertIn("argument", self.cli.commands)

        cmd = self.cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        self.assertIn("datetime_input", params)

        opt = params["datetime_input"]

        assert isinstance(opt.type, click.DateTime)
        self.assertEqual(tuple(opt.type.formats), ("%Y-%m-%dT%H:%M:%SZ",))

    def test_uuid_inputs(self) -> None:
        self.assertIn("argument", self.cli.commands)

        cmd = self.cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        self.assertIn("uuid_input", params)

        opt = params["uuid_input"]

        self.assertEqual(opt.type.name, "uuid")
