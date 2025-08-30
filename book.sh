#!/bin/bash

set -x
# mac
if [ "$(uname)" == "Darwin" ]; then
    host=""mac""
# GNU/Linux操作系统
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    git pull
    host="linux"
# Windows NT操作系统
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    # Windows NT操作系统
    host="windows"
fi

if [ ${host} == "linux" ]; then
    git reset --hard
    git pull
    mdbook build
    cp -r book/* /usr/share/nginx/book/
fi
