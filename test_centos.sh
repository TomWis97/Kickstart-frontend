#!/usr/bin/env bash
set -e
tagname='tomwis97/kickstart-frontend'
echo "Building '$tagname:latest'...:"
#docker rmi $tagname:latest
docker build -t $tagname:latest .
cd os/centos7
#docker rmi -t $tagname:centos7
docker build -t $tagname:centos7 .
docker run -P -ti --rm --network="host" $tagname:centos7
