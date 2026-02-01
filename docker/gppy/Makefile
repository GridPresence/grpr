TARGET := gppy
DOCKR := docker
DKRENVS := "-e MyServer=${DBSRVR} -e MyUser=${DBUSR} -e MyPassword=${DBPSSWD}"
DKRSRCS := "--mount type=bind,src=${MNTSRCS},dest=/home/gppy/Sources,ro"
DKRDEST := "--mount type=bind,src=${MNTDEST},dest=/home/gppy/Playlists"

.PHONY: image
image: installs/gppy_py
		DOCKER_BUILDKIT=1 ${DOCKR} build -t ${TARGET} -f Dockerfile .

.PHONY: clean-image
clean-image:
		DOCKER_BUILDKIT=1 ${DOCKR} build --no-cache -t ${TARGET} -f Dockerfile .

.PHONY: exec
exec:
		${DOCKR} run ${DKRENVS} ${DKRSRCS} ${DKRDEST} ${TARGET}