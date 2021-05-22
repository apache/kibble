# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from unittest import mock

from click.testing import CliRunner

from kibble.cli.commands.scanners_command import scanners_group
from kibble.configuration.yaml_config import kconfig


class TestScannerCommand:
    def test_add(self):
        runner = CliRunner()
        result = runner.invoke(scanners_group, ["add"])

        assert result.exit_code == 0
        assert result.output.strip() == "To be implemented!"

    @mock.patch("kibble.cli.commands.scanners_command.get_scanners_classes")
    def test_list(self, mock_get_scanners_classes):
        class MockScanner:
            pass

        mock_get_scanners_classes.return_value = [MockScanner]
        runner = CliRunner()
        result = runner.invoke(scanners_group, ["list"])

        assert result.exit_code == 0
        assert result.output.strip() == "MockScanner"

    @mock.patch.dict(
        kconfig,
        {
            "data_sources": [
                {
                    "name": "github",
                    "organizations": [{"repo_owner": "apache", "repo_name": "kibble"}],
                    "enabled": ["mock_scanner"],
                }
            ]
        },
    )
    @mock.patch("kibble.cli.commands.scanners_command.get_scanner")
    def test_run(self, mock_get_scanner):
        class MockScanner:
            scanner_name = "mock_scanner"

            def __init__(self, **kwargs):
                pass

            def scan(self):
                pass

        mock_get_scanner.return_value = MockScanner

        runner = CliRunner()
        result = runner.invoke(scanners_group, ["run", "-s", "mock_scanner"])
        assert result.exit_code == 0
        assert (
            result.output.strip() == "Running MockScanner for {'repo_owner': 'apache', 'repo_name': 'kibble'}"
        )
