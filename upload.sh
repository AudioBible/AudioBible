#!/usr/bin/env bash

rm -Rf AudioBible.egg-info && rm -rf dist;
python setup.py register -r pypi && python setup.py sdist upload -r pypi;