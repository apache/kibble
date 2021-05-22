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

from pathlib import Path
from typing import Any, Dict, List, Optional

from kibble.exceptions import KibbleException


def get_scanners(
    data_source: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Automatically discover all scanners. Scanner class is discoverable
    only if it has ``scan`` method. Returns a dictionary where keys are
    scanner types.

    :param data_source: if provided then only scanners for this data source are returned.
    """
    scanner_classes: Dict[str, Any] = {}
    path = Path(__file__).parent
    for file in path.iterdir():
        if file.suffix != ".py" or file.name in ("__init__.py", "base.py"):
            continue
        py_file = file.stem
        mod = __import__(".".join([__name__, py_file]), fromlist=[py_file])
        classes = [cls for x in dir(mod) if isinstance(cls := getattr(mod, x), type) and hasattr(cls, "scan")]
        if data_source:
            classes = [cls for cls in classes if cls.data_source == data_source]  # type: ignore
        for cls in classes:
            scanner_ds = cls.data_source
            scanner_classes[scanner_ds] = scanner_classes.get(scanner_ds, []) + [cls]

    return scanner_classes


def get_scanners_classes(data_source: Optional[str] = None) -> List[Any]:
    """Returns all scanner classes"""
    return sum(get_scanners(data_source).values(), [])


def get_scanner(scanner_name: str):
    """Returns scanner by name"""
    scanners_with_name = [cls for cls in get_scanners_classes() if cls.scanner_name == scanner_name]
    if not scanners_with_name:
        raise KibbleException(f"Scanner with name '{scanner_name}' is undefined")
    return scanners_with_name[0]
