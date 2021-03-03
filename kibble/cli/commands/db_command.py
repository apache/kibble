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

__all__ = ["db_group"]

import click


@click.group(name="db")
def db_group():
    """Manage database"""


@db_group.command(name="init")
def db_init():
    """Initialize database"""
    click.echo("To be implemented!")


def _abort_reset(ctx, _, value):
    if not value:
        ctx.abort()


@db_group.command(name="reset")
@click.option(
    "--yes",
    is_flag=True,
    callback=_abort_reset,
    expose_value=False,
    prompt="This will reset database. Do you want to continue?",
)
def db_reset():
    """Reset database"""
    click.echo("To be implemented!")
