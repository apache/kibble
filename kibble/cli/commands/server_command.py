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

__all__ = ["server_group"]

import click
import uvicorn

from kibble.utils.ascii import KIBBLE_ASCII


@click.group(name="server")
def server_group():
    """API server commands"""


@server_group.command()
def start():
    """Start API server"""
    click.echo(KIBBLE_ASCII)
    click.echo("Using unvicorn for development.\n")
    click.echo("For production deployment consider using gunicorn server:\n")
    click.echo('  gunicorn "kibble.server.app:create_app()" -k "uvicorn.workers.UvicornWorker"')
    click.echo()

    uvicorn.run(
        app="kibble.server.app:create_app",
        factory=True,
        host="127.0.0.1",
        port=1324,
        log_level="info",
    )
