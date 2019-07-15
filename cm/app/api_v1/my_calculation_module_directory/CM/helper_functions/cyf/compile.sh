#!/bin/bash

rm -r /tmp/cyf
mkdir /tmp/cyf
cp -r * /tmp/cyf/
cd /tmp/cyf

ABSOLUTE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
echo $ABSOLUTE_PATH
python $ABSOLUTE_PATH/compile_cython_files.py build_ext --inplace

cd -

cp -r /tmp/cyf/* .

