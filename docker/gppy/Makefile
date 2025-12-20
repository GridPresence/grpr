TARGET := gppy
DOCKR := docker


.PHONY: image
image:
		DOCKER_BUILDKIT=1 ${DOCKR} build -t ${TARGET} -f Dockerfile .

.PHONY: clean-image
clean-image:
		DOCKER_BUILDKIT=1 ${DOCKR} build --no-cache -t ${TARGET} -f Dockerfile .

.PHONY: exec
exec:
		${DOCKR} run -e GPPY_PY=1 ${TARGET} 