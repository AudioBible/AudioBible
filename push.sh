#!/usr/bin/env bash

version=`audiobible/__init__.py version`

git add images/;

echo "## Welcome to [http://audiobible.life](http://audiobible.life) - [KJV](https://github.com/AudioBible/KJV) - [AudioBible](https://github.com/AudioBible/AudioBible)" > IMAGES.md;
echo "" >> IMAGES.md;
echo "[![thomas-jefferson-educate-and-inform-the-masses-quote](images/thomas-jefferson-educate-and-inform-the-masses-quote.png)](https://www.youtube.com/watch?v=72Lrz0khXP0)" >> IMAGES.md;
echo "" >> IMAGES.md;
echo "IMAGES" >> IMAGES.md;
echo "======" >> IMAGES.md;
echo "" >> IMAGES.md;

for i in `ls -1 images/|grep -v youtube-channel|grep -v youtube-search|xargs`; do echo "- [$i](images/$i)" >> IMAGES.md && echo "" >> IMAGES.md && echo "![$i](images/$i)" >> IMAGES.md && echo "" >> IMAGES.md; done

echo "![stats](https://c.statcounter.com/11395037/0/cbecb5be/0/)" >> IMAGES.md;
echo "" >> IMAGES.md;

git commit -am 'update';

if [ -d ~/KJV ]; then
    cp *.md ~/KJV/
    cp images/*.jpg ~/KJV/images/
    cp images/*.jpeg ~/KJV/images/
    cp images/*.png ~/KJV/images/
    cp images/*.gif ~/KJV/images/
    d=`pwd`
    cd ~/KJV && echo "$version" > version && git add version images/* *.md *.json && git commit -am 'update' && git push -f; cd "$d"
fi


git fetch && git rebase origin/master master && git push && git push --tags
git push ysfe -f && git push ysfe --tags -f
git push abl -f && git push abl --tags -f
git push up -f && git push up --tags -f
git push ab -f && git push up --tags -f
git push bb -f && git push bb --tags -f
git push sf -f && git push sf --tags -f
