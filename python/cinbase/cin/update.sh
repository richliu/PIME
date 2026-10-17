#!/bin/bash
cd "$(dirname "$0")" || exit 1

TARGET=/home/richliu

rm -f $TARGET/dayi4.json
rm -f $TARGET/dayi4-add3.json
python3 dayi4to3.py
cd ../tools/
python3 cintojson.py
cd ../json/
cp dayi4.json $TARGET/
cp dayi4-add3.json $TARGET/
# 只還原有追蹤的檔案；用 * 會因為未追蹤的 dayi4-add3.json 整個失敗
git checkout -- .
cd ../tools

