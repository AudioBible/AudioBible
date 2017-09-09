#!/usr/bin/env bash

quality="${1:-"77"}";
quality="$(($quality + 0))";

if [ "$quality" == "0" ]; then
    quality=77;
fi

trap sigint_handler SIGINT

function sigint_handler(){
    rm -Rf ./original_images/optimized/;
    exit 1;
}

echo "+ Optimizing image quality to be $quality%";

if [ -d "./original_images/" ]; then
    cd ./original_images/;

    if [ ! -d "./optimized" ]; then
        echo "+ Creating ./original_images/optimized/ directory";
        mkdir optimized;
    fi

    if [ -d "./optimized" ]; then
        echo "+ Optimizing *.jpg files";
        for i in *.jpg; do convert "$i" -strip -quality "$quality" "optimized/$i"; done
        if [ "$?" == "0" ]; then
            echo "+ Finished with *.jpg files";
        else
            echo "! Failed optimizing *.jpg files";
            exit 1;
        fi
        echo "+ Optimizing *.jpeg files";
        for i in *.jpeg; do convert "$i" -strip -quality "$quality" "optimized/$i"; done
        if [ "$?" == "0" ]; then
            echo "+ Finished with *.jpeg files";
        else
            echo "! Failed optimizing *.jpeg files";
            exit 1;
        fi
        echo "+ Optimizing *.png files";
        for i in *.png; do convert "$i" -strip -quality "$quality" "optimized/$i"; done
        if [ "$?" == "0" ]; then
            echo "+ Finished with *.png files";
        else
            echo "! Failed optimizing *.png files";
            exit 1;
        fi
    fi

    cd ..;

    if [ -d "./original_images/optimized" ]; then
        echo "+ Moving images from ./original_images/optimized/ to ./images/";
        mv ./original_images/optimized/* ./images;
        cp ./original_images/*.gif ./images;
        echo "+ Removing ./original_images/optimized/ directory";
        rm -Rf ./original_images/optimized/;
    fi
else
    echo "! ERROR: ./original_images/ directory does not exist!";
fi