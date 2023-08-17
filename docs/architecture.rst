 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0

 .. Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

Apache Kibble Overview
======================

Kibble configuration
--------------------

Currently Apache Kibble is configured using `kibble.yaml` configuration file.

Database configuration
......................

.. code-block::

    elasticsearch:
      hosts:
        - http://localhost:9200

Data sources configuration
..........................

Multiple data sources can be configured. Each data source is defined by a python class. Additionally to that users
have to pass ``name`` and ``config`` which is a configuration specific for a given data source.

.. code-block::

    data_sources:
      - name: name
        class: path.to.a.Class
        config:
          # Data source specific configuration

Data source
-----------

Data source represents an external source of information (for example Github, JIRA, mailing list etc). Each data source
is a python package. In this way users can easily build their own data sources and use them with Kibble.

Data source package has to have the following structure:

.. code-block::

    data_source_name/
    | __init__.py
    | ...
    | data_types
    | | __init__.py
    | | type1.py
    | | type2.py
    | | ...

The ``data_source_name.__init__`` should include the class defining the data source but the class can be placed in another
file in top leve directory of the package.

Data types
..........

Data type represents a single type of data within a data source. For example if Github is a data source then issues and
comments will be two different data types. A data type is a class that has to implement ``fetch_data`` method that is
used to fetch and persist data.

Data types are automatically determined using data source class path.

Each data type is an index in Kibble elasticsearch instance. The data should be stored "as is" so users can leverage existing
documentation.

Next to persisting data, a data type should also define metrics that can be calculate on retrieved data.

Configuring a data source
.........................

As described previously data sources can be configured in ``kibble.yaml`` config file. For example:

.. code-block::

    data_sources:
      - name: kibble_github
        class: kibble.data_sources.github.GithubDataSource
        config:
          repo_owner: apache
          repo_name: kibble
          enabled_data_types:
            - issues
            - discussions

      - name: pulsar_github
        class: kibble.data_sources.github.GithubDataSource
        config:
          repo_owner: apache
          repo_name: pulsar
          enabled_data_types:
            - issues
            - comments

      - name: pulsar_dev_list
        class: kibble.data_sources.pony.PonyDataSource
        config:
          list_name: dev@pulsar.apache.org
          enabled_data_types:
            - threads

In the above example we can see that:

* We configured two different data sources based on ``GithubDataSource``: apache/pulsar and apache/kibble Github repositories.
  For both sources we fetch different information. For Kibble we fetch issues and discussions data while for Apache
  Pulsar we fetch issues and comments data.
* There's also a third data source using ``PonyDataSource`` configured for Apache Pulsar dev list.

Thanks to this design users will gain more granularity to configure the data they want to fetch. This also creates a big
opportunity for configuring different authorization options for each data source in future.
