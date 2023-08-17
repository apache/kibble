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

from typing import Optional

from kibble.data_sources.base.base_data_source import BaseDataSource
from kibble.exceptions import KibbleException
from kibble.secrets.env_variable import get_secret_from_env


class GithubDataSource(BaseDataSource):
    """Github datasource class"""

    name = "github"

    def __init__(self, *, repo_owner: str, repo_name: str, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_key = api_key or get_secret_from_env("GH_API_KEY")
        if not self.api_key:
            raise KibbleException("No Github API_KEY")
