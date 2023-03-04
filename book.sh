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
    cp -r book/* /usr/share/nginx/book/
    cp -r yisoft.png /usr/share/nginx/book/favicon.ico
    cp -r yisoft.png /usr/share/nginx/book/favicon.png
fi
