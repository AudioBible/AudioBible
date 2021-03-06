#!/usr/bin/env bash

# ./push.sh
# ./push.sh t
# ./push.sh f README,IMAGES
# ./push.sh f README.md,IMAGES.md

trap sigint_handler SIGINT

function sigint_handler(){
    exit 1;
}

version=`audiobible/__init__.py version`
message="BIG BANG IS THEORY! FLAT EARTH IS TRUTH! 9/11 WAS AN INSIDE JOB!"
skip_images="`echo ${1:-"false"} | tr [a-z] [A-Z]`";
skip_files="`echo ${2:-"none"} | tr "," "|"|sed "s/ //g"`";

function WRITE_IMAGES_FILE() {
    local proceed="no";
    local original_images="`ls -1 original_images/|grep -v youtube-channel|grep -v youtube-search|xargs`";
    local images="`ls -1 images/|grep -v youtube-channel|grep -v youtube-search|xargs`";
    if [ "$original_images" != "$images" ]; then
        if [[ $skip_images != *"F"* ]]; then
            ./optimize_images.sh;
        else
            echo "+ Skipping optimize_images";
        fi
    else
        echo "+ No images found to optimize!";
    fi

    for i in $images; do
        if [ "`grep -i "$i" IMAGES.md`" == "" ]; then
            local proceed="yes";
        fi
    done

    if [ "$proceed" == "yes" ]; then
        echo "+ Writing IMAGES.md"
        echo "" > IMAGES.md;
        echo "## ![stats](https://c.statcounter.com/11395037/0/cbecb5be/0/) Welcome to [http://audiobible.life](http://audiobible.life) - Therefore Choose Life - [They Live](https://www.youtube.com/watch?v=JI8AMRbqY6w)" >> IMAGES.md;
        echo "" >> IMAGES.md;
        echo "[README](README.md) | [USAGE](USAGE.md) | [HELP](HELP.md) | [DEVELOPMENT](DEVELOPMENT.md) | [CHANGES](CHANGES.md) | **We The People** | **Have The Power** | **Don't Be A Clown**" >> IMAGES.md;
        echo "" >> IMAGES.md;
        echo "[VIDEOS](VIDEOS.md) | [MUSIC](MUSIC.md) | [CHANNELS](CHANNELS.md) | [DOCUMENTS](DOCUMENTS.md) | [IMAGES](IMAGES.md) | [BOOKS](BOOKS.md) | [LINKS](LINKS.md) | [INFO](INFO.md) | **Join The Revolution**" >> IMAGES.md;
        echo "" >> IMAGES.md;
        echo "IMAGES" >> IMAGES.md;
        echo "======" >> IMAGES.md;
        echo "" >> IMAGES.md;

        for i in $images; do
            echo "- [$i](images/$i)" >> IMAGES.md;
            echo "" >> IMAGES.md;
            echo "![$i](images/$i)" >> IMAGES.md;
            echo "" >> IMAGES.md;
        done
    fi
}

function UPDATE_MODIFIED_DATETIME() {
    if [ "$1" != "" ] && [ "$1" != "none" ];then
        local file_name="$1";
        local file_data="`cat "$file_name"|grep -v "Last Modified: "`";
        local modified_date="`date -r "$file_name" -u`";

        if [ "`head -n 1 "$file_name" | grep -v "$modified_date"`" == "" ]; then
            echo "+ Updating Last Modified DateTime in $file_name to $modified_date";
            echo "Last Modified: $modified_date" > "$file_name";
            echo "$file_data" >> "$file_name";
        fi
    fi
}

if [ "`echo "$skip_files" | grep -v IMAGES`" != "" ]; then
    WRITE_IMAGES_FILE;
fi

for f in `ls -1 *.md| grep -Ev "$skip_files"|xargs`; do
    #cat "$f" | sed '/./,$!d' | awk 'NR > 1 { print prev } { prev=$0 } END { ORS=""; print }'
    if [ -f "$f" ]; then
        UPDATE_MODIFIED_DATETIME "$f";
    fi

    if [ -f "$f.md" ]; then
        UPDATE_MODIFIED_DATETIME "$f.md";
    fi

done

git add original_images/ images/ books/ *.md;
git commit -am "$message";

echo "+ Start PUSH to origin";
git fetch && git rebase origin/master master && git push && git push --tags;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to origin";
else
    echo "! Failed PUSH to origin";
    exit 1;
fi

if [ -d ~/KJV ]; then
    cp *.md ~/KJV/
    cp images/*.jpg ~/KJV/images/
    cp images/*.jpeg ~/KJV/images/
    cp images/*.png ~/KJV/images/
    cp images/*.gif ~/KJV/images/
    d=`pwd`
    echo "+ Start PUSH to KJV origin";
    cd ~/KJV && echo "$version" > version && git add version images/* *.md *.json && git commit -am "$message" && git push -f; cd "$d"
    if [ "$?" == "0" ]; then
        echo "+ Finish PUSH to KJV origin";
    else
        echo "! Failed PUSH to KJV origin";
        exit 1;
    fi
fi

#git push ab -f && git push ab --tags -f;
#if [ "$?" == "0" ]; then
#    echo "+ Finish PUSH to ab";
#else
#    echo "! Failed PUSH to ab";
#    exit 1;
#fi

echo "+ Start PUSH to abl";
git push abl -f && git push abl --tags -f;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to abl";
else
    echo "! Failed PUSH to abl";
    exit 1;
fi

echo "+ Start PUSH to up";
git push up -f && git push up --tags -f;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to up";
else
    echo "! Failed PUSH to up";
    exit 1;
fi

echo "+ Start PUSH to ux";
git push ux -f && git push ux --tags -f;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to ux";
else
    echo "! Failed PUSH to ux";
    exit 1;
fi

echo "+ Start PUSH to ysfe";
git push ysfe -f && git push ysfe --tags -f;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to ysfe";
else
    echo "! Failed PUSH to ysfe";
    exit 1;
fi

echo "+ Start PUSH to bb";
git push bb -f && git push bb --tags -f;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to bb";
else
    echo "! Failed PUSH to bb";
    exit 1;
fi

echo "+ Start PUSH to gl";
git push gl -f && git push gl --tags -f;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to gl";
else
    echo "! Failed PUSH to gl";
    exit 1;
fi

echo "+ Start PUSH to sf";
git push sf -f && git push sf --tags -f;
if [ "$?" == "0" ]; then
    echo "+ Finish PUSH to sf";
else
    echo "! Failed PUSH to sf";
    exit 1;
fi
