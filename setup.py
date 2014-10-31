#!/usr/bin/env python

__author__ = 'Yuta Hayashibe' 
__version__ = ""
__copyright__ = ""
__license__ = "GPL v3"

import os
version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(version_file) as fh:
    pyknp_version = fh.read().strip()


from setuptools import setup, find_packages, Extension
setup(
    name = "knp",
    version = pyknp_version,
    maintainer = "Yuta Hayashibe",
    maintainer_email = "yuta@hayashibe.jp",
    author = "Yuta Hayashibe",
    author_email = "yuta@hayashibe.jp",
    description = "KNP bindings for Python.",
    license = "GNU GENERAL PUBLIC LICENSE Version 3",
    url = "https://github.com/shirayu/pyknp",
    packages = find_packages(),
)

