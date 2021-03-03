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


@click.group(name="scanners")
def scanners_group():
    """Configure and trigger scanners"""


@scanners_group.command()
def add():
    """Add new scanner configuration"""
    click.echo("To be implemented!")


@scanners_group.command(name="list")
def list_scanners():
    """List all available scanners"""
    scanners_list = ["AbcScanner", "XyzeScanner"]
    for scanner in scanners_list:
        click.echo(f"- {scanner}")


@scanners_group.command()
@click.argument("scanner_name")
def run(scanner_name: str):
    """Trigger a scanning process for given scanner"""
    click.echo(f"Running {scanner_name}")
