#!/bin/bash
docker run -it --rm -e USERID=`id -u` -e GROUPID=`id -g` -e UMASK=022 -e USER=actionet `pwd`:/home/actionet -p 8787:8787 -v actionet/actionet:mro


