#!/bin/bash

set -x

mdbook build
cp -r baidu_verify_codeva-5WexnefSpS.html book/
cp -r BingSiteAuth.xml book/
cp -r book/* /usr/share/nginx/book/
