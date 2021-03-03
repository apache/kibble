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

import click

from kibble.cli.commands.config_command import config_group
from kibble.cli.commands.db_command import db_group
from kibble.cli.commands.scanners_command import scanners_group
from kibble.cli.commands.server_command import server_group
from kibble.cli.commands.version_command import version_cmd


@click.group()
def cli():
    """Manage and configure Apache Kibble instance."""


# Try to keep this list sorted A-Z
cli.add_command(config_group)
cli.add_command(db_group)
cli.add_command(server_group)
cli.add_command(scanners_group)
cli.add_command(version_cmd)
