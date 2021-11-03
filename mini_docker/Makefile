PARENT_DOCKER=actionet/actionet:mini
REGISTRY=actionet
IMAGE_NAME=actionet
VERSION=mini
all: build

build:
	DOCKER_BUILDKIT=1 docker build \
	  --tag ${IMAGE_NAME}:${VERSION} \
	  --tag ${REGISTRY}/${IMAGE_NAME}:${VERSION} \
	  --build-arg BUILDKIT_INLINE_CACHE=1 \
	  .

test:
	docker run -it -e USER=user -e PASSWORD=password -e USERID=1000 -e GROUPID=1000 -e UMASK=022 -p 8888:8888  --rm  $(IMAGE_NAME):${VERSION}

