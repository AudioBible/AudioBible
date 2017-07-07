#!/usr/bin/env bash

cp *.md ~/KJV/ && git add *.md
cp images/*.jpg ~/KJV/images/
cp images/*.png ~/KJV/images/
cp images/*.gif ~/KJV/images/
d=`pwd`
cd ~/KJV && git add images/* && git commit -am 'update' && git push; cd "$d"

git push && git push --tags
git push ysfe && git push ysfe --tags
git push up && git push up --tags
git push bb && git push bb --tags
git push sf && git push sf --tags
