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

from click.testing import CliRunner

from kibble.cli.commands.db_command import db_group


class TestDbCommand:
    def test_init(self):
        runner = CliRunner()
        result = runner.invoke(db_group, ["init"])

        assert result.exit_code == 0
        assert result.output.strip() == "To be implemented!"

    def test_reset_no(self):
        runner = CliRunner()
        result = runner.invoke(db_group, ["reset"], input="N")

        msg = "This will reset database. Do you want to continue? [y/N]: N\nAborted!"
        assert result.output.strip() == msg
        assert result.exit_code == 1

    def test_reset_yes(self):
        runner = CliRunner()
        result = runner.invoke(db_group, ["reset", "--yes"])

        assert result.exit_code == 0
        assert result.output.strip() == "To be implemented!"
