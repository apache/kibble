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

from typing import Optional

import click

from kibble.configuration.yaml_config import kconfig
from kibble.scanners import get_scanner, get_scanners_classes


@click.group(name="scanners")
def scanners_group():
    """Configure and trigger scanners"""


@scanners_group.command()
def add():
    """Add new scanner configuration"""
    click.echo("To be implemented!")


@scanners_group.command(name="list")
@click.option("-ds", "--data-source")
def list_scanners(data_source: Optional[str] = None):
    """List all available scanners"""
    all_scanners = get_scanners_classes(data_source)
    for scanner in sorted(all_scanners, key=lambda cls: cls.__name__):
        click.echo(f"{scanner.__name__}")


@scanners_group.command()
@click.option("-s", "--scanner-name", required=True)
def run(scanner_name: str):
    """Trigger a scanning process for given scanner"""
    for data_source in kconfig.get("data_sources", []):
        if scanner_name not in data_source["enabled"]:
            continue
        organizations = data_source.get("organizations", [])
        if not organizations:
            click.echo(f"No organizations to scan in {data_source} data source.")
            continue

        scanner = get_scanner(scanner_name=scanner_name)
        for org in organizations:
            click.echo(f"Running {scanner.__name__} for {org}")
            scanner(**org).scan()
