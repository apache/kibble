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

import inspect
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

from kibble.data_sources.base.base_data_type import BaseDataType
from kibble.data_sources.base.module_loading import import_string


class BaseDataSource:
    """Base class for all data sources"""

    _data_types_folder = "data_types"
    _excluded_files = {"base"}

    def __init__(self, *, enabled_data_types: Optional[List[str]] = None):
        self.enabled_data_types = enabled_data_types

    def _get_data_type_classes(self) -> Dict[str, str]:
        data_source_path = Path(inspect.getfile(self.__class__))
        data_types_dir = data_source_path.parent.joinpath(self._data_types_folder)
        data_type_classes = {}

        for file in data_types_dir.iterdir():
            if file.stem in self._excluded_files or file.stem.startswith("_"):
                continue
            data_type_classes[file.stem] = f"{self.__module__}.{self._data_types_folder}.{file.stem}.DataType"
        return data_type_classes

    @cached_property
    def data_types_classes(self) -> Dict[str, str]:
        """Returns data types defined in this data source"""
        return self._get_data_type_classes()

    def scan(self):
        """Collect data for configured data types"""
        unscanned = []
        if not self.enabled_data_types:
            print("No data types enabled")
            return

        for data_type_name in self.enabled_data_types:
            klass = self.data_types_classes.get(data_type_name)
            if not klass:
                unscanned.append(data_type_name)
                continue
            data_type_class = import_string(klass)
            data_type: BaseDataType = data_type_class(data_source=self)
            data_type.fetch_data()

        if unscanned:
            print(f"Found no data types for following configurations {unscanned}")


class DataSourceConfig(NamedTuple):
    """Data source configuration"""

    name: str
    klass: str
    config: Dict[str, Any]

    @classmethod
    def from_dict(cls, dictionary: Dict):
        """Make DataSourceConfig from a dictionary"""
        return cls(
            name=dictionary["name"],
            klass=dictionary["class"],
            config=dictionary["config"],
        )

    def get_object(self) -> BaseDataSource:
        """Return data source object defined by this config"""
        ds_class = import_string(self.klass)
        return ds_class(**self.config)
