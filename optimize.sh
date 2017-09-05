#!/usr/bin/env bash

quality="${1:-"77"}";
quality="$(($quality + 0))";

if [ "$quality" == "0" ]; then
    quality=77;
fi

echo "optimizing image quality to be $quality%";

if [ -d "./original_images/" ]; then
    cd ./original_images/;

    if [ ! -d "./optimized" ]; then
        echo "creating ./original_images/optimized/ directory";
        mkdir optimized;
    fi

    if [ -d "./optimized" ]; then
        echo "optimizing *.jpg files";
        for i in *.jpg; do convert "$i" -strip -quality "$quality" "optimized/$i"; done
        echo "optimizing *.jpeg files";
        for i in *.jpeg; do convert "$i" -strip -quality "$quality" "optimized/$i"; done
        echo "optimizing *.png files";
        for i in *.png; do convert "$i" -strip -quality "$quality" "optimized/$i"; done
    fi

    cd ..;

    if [ -d "./original_images/optimized" ]; then
    echo "moving images from ./original_images/optimized/ to ./images/";
    mv ./original_images/optimized/* ./images;
    cp ./original_images/*.gif ./images;
        echo "removing ./original_images/optimized/ directory";
        rm -Rf ./original_images/optimized/;
    fi
else
    echo "ERROR: ./original_images/ directory does not exist!";
fi