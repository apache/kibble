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

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode, urljoin

import requests

from kibble.scanners.base import BaseScanner
from kibble.secrets.env_variable import get_secret_from_env


class GithubBaseScanner(BaseScanner):
    """Github base scanner class"""

    # pylint: disable=too-few-public-methods
    data_source = "github"

    def __init__(self, *, repo_owner: str, repo_name: str, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_key = api_key or get_secret_from_env("GH_API_KEY")
        self.repo_full_name = f"{self.repo_owner}/{self.repo_name}"

        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if api_key:
            self.headers["Authorization"] = f"token {api_key}"

    def _send_request(self, endpoint: str, query: Optional[Dict] = None) -> Union[List, Dict]:
        url = urljoin(self.base_url, endpoint)
        url = f"{url}?{urlencode(query)}" if query else url
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _persist(self, payload: Any):
        pass


class GithubIssuesScanner(GithubBaseScanner):
    """Github issues and pull requests scanner"""

    scanner_name = "github_issues"

    def scan(self):
        endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/issues"
        query = {"per_page": 100, "page": 1}

        issues: List[Dict] = []
        prs: List[Dict] = []
        self.log.info("Collecting Github issues and PRs from %s", self.repo_full_name)
        while new_issues := self._send_request(endpoint, query):
            for issue_pr in new_issues:
                if "pull_request" in issue_pr:
                    prs.append(issue_pr)
                else:
                    issues.append(issue_pr)
            query["page"] += 1

        self.log.info("Collected %d issues and %d PRs from %s", len(issues), len(prs), self.repo_full_name)
        return issues, prs
