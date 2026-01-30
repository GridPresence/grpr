TARGET := rungrpr
# DOCKR := podman

.PHONY: image
image:
		${DOCKR} build -t ${TARGET} -f Dockerfile .

.PHONY: clean-image
clean-image:
		${DOCKR} build --no-cache -t ${TARGET} -f Dockerfile .