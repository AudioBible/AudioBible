#!/usr/bin/env bash

version=`audiobible/__init__.py version`
git commit -am "update version to $version"
git tag -a "$version" -m "$version"
./upload.sh
./push.sh
