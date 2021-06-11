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

from typing import Dict, List, Optional, Union
from urllib.parse import urlencode, urljoin

import requests

from kibble.data_sources.base.base_data_type import BaseDataType
from kibble.data_sources.github import GithubDataSource


# pylint: disable=abstract-method
class GithubBaseDataType(BaseDataType):
    """Base data type class for Github"""

    _index = "github"

    def __init__(self, *, data_source: GithubDataSource, **kwargs):
        super().__init__(**kwargs)

        self.repo_owner = data_source.repo_owner
        self.repo_name = data_source.repo_name
        self.repo_full_name = f"{self.repo_owner}/{self.repo_name}"

        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {data_source.api_key}",
        }

    def _send_request(self, endpoint: str, query: Optional[Dict] = None) -> Union[List, Dict]:
        url = urljoin(self.base_url, endpoint)
        url = f"{url}?{urlencode(query)}" if query else url
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
