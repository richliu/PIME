
TARGET=/home/richliu

rm -f $TARGET/dayi4.json
rm -f $TARGET/dayi4-add3.json
python3 dayi4to3.py
cd ../tools/
python3 cintojson.py
cd ../json/
cp dayi4.json $TARGET/
cp dayi4-add3.json $TARGET/
git reset *
cd ../tools

