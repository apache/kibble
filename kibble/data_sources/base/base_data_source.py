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

from typing import Dict, List, Optional

from kibble.data_sources.base.module_loading import import_string


class BaseDataSource:
    """Base class for all data sources"""

    data_types_classes: Dict[str, str] = {}

    def __init__(self, *, enabled_data_types: Optional[List[str]] = None):
        self.enabled_data_types = enabled_data_types

    def scan(self):
        """Collect data for configured data types"""
        for data_type_name, klass in self.data_types_classes.items():
            if self.enabled_data_types and data_type_name not in self.enabled_data_types:
                continue
            data_type_class = import_string(klass)
            data_type = data_type_class(data_source=self)
            data_type.scan()
