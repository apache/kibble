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

from setuptools import find_packages, setup

VERSION = "2.0.0dev"

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

DEVEL_REQUIREMENTS = [
    "black==20.8b1",
    "pre-commit==2.7.1",
    "pylint==2.6.2",
    "pytest==6.1.1",
]

INSTALL_REQUIREMENTS = ["requests>=2.25.1"]

EXTRAS_REQUIREMENTS = {"devel": DEVEL_REQUIREMENTS}


def get_long_description() -> str:
    """Retrieves package description from README.md"""
    try:
        with open(os.path.join(BASE_PATH, "README.md")) as file:
            description = file.read()
    except FileNotFoundError:
        description = ""
    return description


def do_setup() -> None:
    """Perform the Kibble package setup."""
    setup(
        name="apache-kibble",
        description="Apache Kibble is a tool to collect, aggregate and "
        "visualize data about any software project.",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        license="Apache License 2.0",
        version=VERSION,
        packages=find_packages(include=["kibble*"]),
        package_data={"kibble": ["py.typed"]},
        include_package_data=True,
        zip_safe=False,
        entry_points={"console_scripts": ["kibble = kibble.__main__:main"]},
        install_requires=INSTALL_REQUIREMENTS,
        setup_requires=["docutils", "gitpython", "setuptools", "wheel"],
        extras_require=EXTRAS_REQUIREMENTS,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.8",
        ],
        author="Apache Software Foundation",
        author_email="dev@kibble.apache.org",
        url="https://kibble.apache.org/",
        download_url=f"https://archive.apache.org/dist/kibble/{VERSION}",
        test_suite="setup.kibble_test_suite",
        python_requires="~=3.8",
        project_urls={
            "Documentation": "https://kibble.apache.org/docs/",
            "Bug Tracker": "https://github.com/apache/kibble/issues",
            "Source Code": "https://github.com/apache/kibble",
        },
    )


if __name__ == "__main__":
    do_setup()
