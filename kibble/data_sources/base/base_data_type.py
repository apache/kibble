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

import logging
from typing import Any, Dict, List, Optional

from elasticsearch import RequestError

from kibble.database.connection import es
from kibble.exceptions import KibbleException


class BaseDataType:
    """Abstract, base class for all data types"""

    _index: Optional[str]

    def __init__(self, **kwargs):
        self.log = logging.getLogger(__name__)

    def fetch_data(self):  # pylint: disable=no-self-use
        """Fetch data from data source"""
        raise NotImplementedError()

    def persist(self, payload: List[Any], doc_type: str, id_mapper):
        """
        Persists the payload in data type index

        :param payload: List of documents to be persisted in ES
        :param doc_type: Name of the document to be used
        :param id_mapper: Function that takes a single document and retrieves its id that will
            be used as document ID in ES.
        """
        if not self._index:
            raise KibbleException(f"Data type {self.__class__.__name__} has no index defined")

        if not id_mapper:
            raise KibbleException("id_mapper has to be specified to created id for document")

        try:
            es.indices.create(index=self._index)
        except RequestError as err:
            if err.error != "resource_already_exists_exception":
                raise

        for document in payload:
            es.index(index=self._index, doc_type=doc_type, body=document, id=id_mapper(document))

    def read(self, query: Optional[Dict[str, Any]] = None):
        """Read data from data type index"""
        query = query or {"match_all": {}}
        return es.search(index=self._index, body={"query": query})
