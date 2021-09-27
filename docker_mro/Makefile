PARENT_DOCKER=actionet/actionet:mro
REGISTRY=actionet
IMAGE_NAME=actionet
VERSION=mro
all: build

build:
	docker build \
	  --tag $(IMAGE_NAME):${VERSION} --tag $(REGISTRY)/$(IMAGE_NAME):${VERSION} -t $(IMAGE_NAME) .
test:
	docker run -it --rm -e USERID=1000 -e GROUPID=1000 -e UMASK=022 -p 8787:8787 -v `pwd`:/scratch $(REGISTRY)/$(IMAGE_NAME):${VERSION}


