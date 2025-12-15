TARGET := gpcpp
DOCKR := podman


.PHONY: image
image:
		DOCKER_BUILDKIT=1 ${DOCKR} build -t ${TARGET} -f Dockerfile .

.PHONY: clean-image
clean-image:
		DOCKER_BUILDKIT=1 ${DOCKR} build --no-cache -t ${TARGET} -f Dockerfile .