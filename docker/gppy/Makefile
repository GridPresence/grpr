TARGET := gppy
T1 := catalog
T2 := playgen
T3 := proto

DOCKR ?= docker

DKRENVS := -e MyServer=${DBSRVR} -e MyUser=${DBUSR} -e MyPassword=${DBPSSWD} -e MyDb=${DBNAME}
DKRSRCS := --mount type=bind,src=${MNTSRCS},dst=/home/gppy/Sources,ro
DKRDEST := --mount type=bind,src=${MNTPLAYS},dst=/home/gppy/Playlists

.PHONY: catalog
catalog: installs/gppy_catalog
		DOCKER_BUILDKIT=1 ${DOCKR} build -t ${TARGET}-${T1} -f ${T1}.dockerfile .

.PHONY: clean-catalog
clean-catalog:
		DOCKER_BUILDKIT=1 ${DOCKR} build --no-cache -t ${TARGET}-${T1} -f ${T1}.dockerfile .

.PHONY: exec-catalog
exec-catalog:
		${DOCKR} run ${DKRENVS} ${DKRSRCS} ${DKRDEST} ${TARGET}-${T1}

.PHONY: playgen
playgen: installs/gppy_playgen
		DOCKER_BUILDKIT=1 ${DOCKR} build -t ${TARGET}-${T2} -f ${T2}.dockerfile .

.PHONY: clean-playgen
clean-playgen:
		DOCKER_BUILDKIT=1 ${DOCKR} build --no-cache -t ${TARGET}-${T2} -f ${T2}.dockerfile .

.PHONY: exec-playgen
exec-playgen:
		${DOCKR} run ${DKRENVS} ${DKRSRCS} ${DKRDEST} ${TARGET}-${T2}

.PHONY: proto
proto: installs/gppy_playgen
		DOCKER_BUILDKIT=1 ${DOCKR} build -t ${TARGET}-${T3} -f ${T3}.dockerfile .

.PHONY: clean-proto
clean-proto:
		DOCKER_BUILDKIT=1 ${DOCKR} build --no-cache -t ${TARGET}-${T3} -f ${T3}.dockerfile .

.PHONY: exec-proto
exec-proto:
		${DOCKR} run ${DKRENVS} ${TARGET}-${T3}

.PHONY: clean
clean: clean-proto clean-catalog clean-playgen

.PHONY: all
all: catalog playgen
