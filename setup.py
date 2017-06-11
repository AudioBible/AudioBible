# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from audiobible import __version__

setup(
    name="AudioBible",
    version=__version__,
    description="KJV Audio Bible",
    long_description="King James Version Audio Bible - download, listen, read and find verses using search",
    license="MIT",
    maintainer="Alex Goretoy",
    maintainer_email="alex@goretoy.com",
    url="https://github.com/gxela/AudioBible",

    packages=find_packages(),
    install_requires=['scrapy'],
    entry_points={
        'console_scripts': [
            'audiobible=audiobible:use_parse_args',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
