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

import os
from typing import Dict

import yaml

KIBBLE_YAML = "kibble.yaml"


def parse_kibble_yaml() -> Dict:
    """Reads kibble.yaml config file"""
    kibble_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    config_path = os.path.join(kibble_base_path, KIBBLE_YAML)
    with open(config_path, "r") as stream:
        config = yaml.safe_load(stream)
    return config


kconfig = parse_kibble_yaml()