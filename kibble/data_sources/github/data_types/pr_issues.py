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

from typing import Any, Dict, List, Tuple

from kibble.data_sources.github.data_types.base import GithubBaseDataType

Issue = Dict[str, Any]
PR = Dict[str, Any]


class GithubPrAndIssuesDataType(GithubBaseDataType):
    """Github issues and pull requests"""

    name = "pr_and_issues"

    def fetch_data(self):
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

    def persist(self, payload: Tuple[List[Issue], List[PR]]):
        issues, prs = payload
        self._persist(issues)
        self._persist(prs)
