# -*- coding: utf-8 -*-
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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

    packages=['audiobible'],
    install_requires=['scrapy'],
    entry_points={
        'console_scripts': [
            'audiobible=audiobible:use_parse_args',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Scrapy",
        "Intended Audience :: Religion",
        "License :: Public Domain",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Religion"
    ]
)
