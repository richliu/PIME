#!/bin/bash
cd "$(dirname "$0")" || exit 1

TARGET=/home/richliu

rm -f $TARGET/dayi4.json
cd ../tools/
python3 cintojson.py
cd ../json/
cp dayi4.json $TARGET/
git checkout -- .
cd ../tools
