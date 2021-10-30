#!/bin/sh

set -e

if [ -d "build" ]
then
    rm -fr build/
fi

mkdir -p build

cp -r flashcards build/app
cp Dockerfile build

cd build/app
mv flashcards.py main.py
rm -fr __pycache__ set_*

cd ..

docker build --tag flaskapp .

