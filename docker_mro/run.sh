#!/bin/bash
export PARENT_DOCKER=shmohammadi86/actionet:mro
export REGISTRY=shmohammadi86
export IMAGE_NAME=actionet
export VERSION=mro
docker run -it --rm -e USERID=1000 -e GROUPID=1000 -e UMASK=022 -p 8787:8787 -v `pwd`:/scratch $(IMAGE_NAME):${VERSION}


