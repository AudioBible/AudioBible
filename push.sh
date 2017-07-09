#!/usr/bin/env bash

if [ -d ~/KJV ]; then
    cp *.md ~/KJV/
    cp images/*.jpg ~/KJV/images/
    cp images/*.png ~/KJV/images/
    cp images/*.gif ~/KJV/images/
    d=`pwd`
    cd ~/KJV && git add images/* && git add *.md && git add *.json && git commit -am 'update' && git push; cd "$d"
fi

git push && git push --tags
git push ysfe && git push ysfe --tags
git push up && git push up --tags
git push bb && git push bb --tags
git push sf && git push sf --tags
