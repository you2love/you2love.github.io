#!/bin/bash

set -x

mdbook build
cp -r book/* /usr/share/nginx/book/
