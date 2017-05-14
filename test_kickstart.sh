#!/usr/bin/env bash
set -e
tagname='tomwis97/kickstart-frontend'
echo "Building '$tagname:latest'...:"
docker build -t $tagname:latest .
docker run -P -ti --rm --network="host" $tagname:latest
