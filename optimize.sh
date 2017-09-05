#!/usr/bin/env bash

cd ./original_images;
mkdir optimized;

for i in *.jpg; do convert "$i" -strip -quality 86 "optimized/$i"; done
for i in *.jpeg; do convert "$i" -strip -quality 86 "optimized/$i"; done
for i in *.png; do convert "$i" -strip -quality 86 "optimized/$i"; done

cd ..;

mv ./original_images/optimized/* ./images;
