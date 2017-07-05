#!/usr/bin/env bash

git push && git push --tags
git push ysfe && git push ysfe --tags
git push up && git push up --tags
git push bb && git push bb --tags
git push sf && git push sf --tags

cp README.md ~/KJV/README.md
cp *.jpg ~/KJV/
cp *.png ~/KJV/
d=`pwd`
cd ~/KJV && git add *.jpg *.png && git commit -am 'update' && git push; cd "$d"
