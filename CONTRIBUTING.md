<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
 -->

# Contributing to Apache Kibble

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of contents**

- [Community](#community)
- [Development installation](#development-installation)
- [Testing](#testing)
- [Code Quality](#code-quality)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Community

The main development and design discussion happens on our mailing lists.
We have a list specifically for development and one for future user questions and feedback.

To join in the discussion on the design and roadmap, you can send an email to [dev@kibble.apache.org](mailto:dev@kibble.apache.org).<br/>
You can subscribe to the list by sending an email to [dev-subscribe@kibble.apache.org](mailto:dev-subscribe@kibble.apache.org).<br/>
You can also browse the archives online at [lists.apache.org](https://lists.apache.org/list.html?dev@kibble.apache.org).

We also have:

- IRC channel, #kibble on [Freenode](https://webchat.freenode.net/?channels=#kibble)
- Slack channel, #kibble on [ASF slack](https://s.apache.org/slack-invite)

## Development installation

You should be able to install Apache Kibble by simply doing:

```
pip install -e ."[devel]"
```

This will install the Kibble package in editable mode together wit all requirements needed for fluent
development.

You may also use the development Docker file:

```
docker build -f Dockerfile.dev -t apache/kibble-dev .
docker run apache/kibble-dev kibble
docker run apache/kibble-dev pytest
```

## Testing

Apache Kibble project uses [pytest](https://docs.pytest.org/en/stable/) for running testing. Writing
good tests help us avoid regression and unexpected issues.

In order to run tests all you need to do is call pytest:

```
# Run all tests
pytest

# Run single test file
pytest tests/cli/commands/test_config_command.py
```

The test can be also run using the dev docker image:

```
➜ docker run apache/kibble pytest tests/cli/commands/test_config_command.py
============================= test session starts ==============================
platform linux -- Python 3.8.8, pytest-6.1.1, py-1.10.0, pluggy-0.13.1 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /kibble, configfile: pyproject.toml
collecting ... collected 1 item

tests/cli/commands/test_config_command.py::TestConfigCommand::test_show PASSED [100%]

============================== 1 passed in 0.02s ===============================
```

## Code Quality

Apache Kibble project is using different tools to ensure the quality of the code, including:

- [black](https://github.com/psf/black)
- [pylint](https://www.pylint.org)
- [isort](https://github.com/PyCQA/isort)
- [mypy](https://github.com/python/mypy)
- [pydocstyle](https://github.com/PyCQA/pydocstyle)

All those tools can be automatically run using [pre-commits](https://pre-commit.com). We encourage you to
use pre-commits, but it's not required to contribute. Every change is checked
on CI and if it does not pass the tests it cannot be accepted. If you want to check locally then
you should install Python3.6 or newer together and run:

```bash
pip install pre-commit
# or
brew install pre-commit
```

For more installation options visit the [pre-commits](https://pre-commit.com).
To turn on pre-commit checks for commit operations in git, run:

```bash
pre-commit install
```

To run all checks on your staged files, run:

```bash
pre-commit run
```

To run all checks on all files, run:

```bash
pre-commit run --all-files
```
