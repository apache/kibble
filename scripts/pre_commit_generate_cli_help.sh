#!/usr/bin/env bash
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

set -euo pipefail

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TMP_FILE=$(mktemp)
TMP_OUTPUT=$(mktemp)

cd "${MY_DIR}/../" || exit;

echo "\`\`\`" >"${TMP_FILE}"

export MAX_SCREEN_WIDTH=100
export FORCE_SCREEN_WIDTH="true"
export VERBOSE="true"

kibble --help | sed 's/^/  /' | sed 's/ *$//' >>"${TMP_FILE}"

echo "\`\`\`" >> "${TMP_FILE}"

MAX_LEN=$(awk '{ print length($0); }' "${TMP_FILE}" | sort -n | tail -1 )

README_FILE="${MY_DIR}/../README.md"

LEAD='^<!-- AUTO_CLI_STAR -->$'
TAIL='^<!-- AUTO_CLI_END -->$'

BEGIN_GEN=$(grep -n "${LEAD}" <"${README_FILE}" | sed 's/\(.*\):.*/\1/g')
END_GEN=$(grep -n "${TAIL}" <"${README_FILE}" | sed 's/\(.*\):.*/\1/g')
cat <(head -n "${BEGIN_GEN}" "${README_FILE}") \
    "${TMP_FILE}" \
    <(tail -n +"${END_GEN}" "${README_FILE}") \
    >"${TMP_OUTPUT}"

mv "${TMP_OUTPUT}" "${README_FILE}"
