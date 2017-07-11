#!/usr/bin/env bash

version=`audiobible/__init__.py version`
if [ -d ~/KJV ]; then
    cp *.md ~/KJV/
    cp images/*.jpg ~/KJV/images/
    cp images/*.jpeg ~/KJV/images/
    cp images/*.png ~/KJV/images/
    cp images/*.gif ~/KJV/images/
    d=`pwd`
    cd ~/KJV && echo "$version" > version && git add version images/* *.md *.json && git commit -am 'update' && git push -f; cd "$d"
fi


git fetch && git rebase origin/master master && git git push && git push --tags
git push ysfe -f && git push ysfe --tags -f
git push up -f && git push up --tags -f
git push bb -f && git push bb --tags -f
git push sf -f && git push sf --tags -f
