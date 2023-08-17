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

__all__ = ["scanners_group"]

import click

from kibble.configuration.yaml_config import kconfig
from kibble.data_sources.base.base_data_source import DataSourceConfig


@click.group(name="scanners")
def scanners_group():
    """Configure and trigger scanners"""


@scanners_group.command()
@click.option("-s", "--data-source", "data_source_name", required=True)
def run(data_source_name: str):
    """Trigger a scanning process for given data source"""
    data_source_config = None
    for ds_in_config in kconfig.get("data_sources", []):
        if ds_in_config["name"] == data_source_name:
            data_source_config = DataSourceConfig.from_dict(ds_in_config)
            break

    if not data_source_config:
        click.echo(f"Data source {data_source_name} not configured")
        return

    data_source = data_source_config.get_object()
    click.echo(f"Scanning {data_source_name}")
    data_source.scan()
