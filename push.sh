#!/usr/bin/env bash

version=`audiobible/__init__.py version`

git fetch && git rebase origin/master master

git add images/;

echo "" >> IMAGES.md;
echo "## ![stats](https://c.statcounter.com/11395037/0/cbecb5be/0/) Welcome to [http://audiobible.life](http://audiobible.life) - Therefore Choose Life" > IMAGES.md;
echo "" >> IMAGES.md;
echo "[README](README.md) | [USAGE](USAGE.md) | [HELP](HELP.md) | [DEVELOPMENT](DEVELOPMENT.md) | [CHANGES](CHANGES.md) | **We The People** | **Have The Power** | **Don't Be A Clown**" >> IMAGES.md;
echo "" >> IMAGES.md;
echo "[VIDEOS](VIDEOS.md) | [MUSIC](MUSIC.md) | [CHANNELS](CHANNELS.md) | [DOCUMENTS](DOCUMENTS.md) | [IMAGES](IMAGES.md) | [BOOKS](BOOKS.md) | [LINKS](LINKS.md) | [INFO](INFO.md) | **Join The Revolution**" >> IMAGES.md;
echo "" >> IMAGES.md;
echo "IMAGES" >> IMAGES.md;
echo "======" >> IMAGES.md;
echo "" >> IMAGES.md;

for i in `ls -1 images/|grep -v youtube-channel|grep -v youtube-search|xargs`; do echo "- [$i](images/$i)" >> IMAGES.md && echo "" >> IMAGES.md && echo "![$i](images/$i)" >> IMAGES.md && echo "" >> IMAGES.md; done

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


git push && git push --tags
git push abl -f && git push abl --tags -f
git push tfcl -f && git push tfcl --tags -f
git push ysfe -f && git push ysfe --tags -f
git push up -f && git push up --tags -f
git push ab -f && git push ab --tags -f
git push bb -f && git push bb --tags -f
git push sf -f && git push sf --tags -f
