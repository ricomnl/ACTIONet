#!/bin/bash
docker run -it --rm -e USERID=1000 -e GROUPID=1000 -e UMASK=022 -p 8787:8787 -v `pwd`:/scratch actionet/actionet:mro


