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
    cp -r baidu_verify_codeva-5WexnefSpS.html book/
    cp -r BingSiteAuth.xml book/
    cp -r yisoft.site.svg book/favicon.svg
    cp -r yisoft.site.png book/favicon.png
    cp -r book/* /usr/share/nginx/book/
fi
