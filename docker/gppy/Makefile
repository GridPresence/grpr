TARGET := gppy
T1 := catalog
T2 := playgen
T3 := proto
T4 := validate

DKRENVS := -e MyServer=${DBSRVR} -e MyUser=${DBUSR} -e MyPassword=${DBPSSWD} -e MyDb=${DBNAME}
DKRSRCS := --mount type=bind,src=${MNTSRCS},dst=/home/gppy/Sources,ro
# DKRDEST := --mount type=bind,src=${MNTPLAYS},dst=/home/gppy/Playlists
DKRVOLCRT := --driver local --opt type=nfs --opt o=addr=192.168.0.73,rw --opt device=:/nfs/Public
DKRVOLMNT := -v nas:/netmnt

.PHONY: nfs
nfs:
		${DOCKER} volume create ${DKRVOLCRT} nas

.PHONY: clean-nfs
clean-nfs:
		${DOCKER} volume rm nas


.PHONY: catalog
catalog: installs/gppy_catalog
		DOCKER_BUILDKIT=1 ${DOCKER} build -t ${TARGET}-${T1} -f ${T1}.dockerfile .

.PHONY: clean-catalog
clean-catalog:
		DOCKER_BUILDKIT=1 ${DOCKER} build --no-cache -t ${TARGET}-${T1} -f ${T1}.dockerfile .

.PHONY: exec-catalog
exec-catalog:
		${DOCKER} run ${DKRENVS} ${DKRVOLMNT} ${TARGET}-${T1}

.PHONY: playgen
playgen: installs/gppy_playgen
		DOCKER_BUILDKIT=1 ${DOCKER} build -t ${TARGET}-${T2} -f ${T2}.dockerfile .

.PHONY: clean-playgen
clean-playgen:
		DOCKER_BUILDKIT=1 ${DOCKER} build --no-cache -t ${TARGET}-${T2} -f ${T2}.dockerfile .

.PHONY: exec-playgen
exec-playgen:
		${DOCKER} run ${DKRENVS} ${DKRVOLMNT} ${TARGET}-${T2}

.PHONY: proto
proto: installs/gppy_playgen
		DOCKER_BUILDKIT=1 ${DOCKER} build -t ${TARGET}-${T3} -f ${T3}.dockerfile .

.PHONY: clean-proto
clean-proto:
		DOCKER_BUILDKIT=1 ${DOCKER} build --no-cache -t ${TARGET}-${T3} -f ${T3}.dockerfile .

.PHONY: exec-proto
exec-proto: proto
		${DOCKER} run ${DKRVOLMNT} -it --rm ${TARGET}-${T3} /bin/ash

.PHONY: validate
validate: installs/gppy_validate
		DOCKER_BUILDKIT=1 ${DOCKER} build -t ${TARGET}-${T4} -f ${T4}.dockerfile .

.PHONY: clean-validate
clean-validate:
		DOCKER_BUILDKIT=1 ${DOCKER} build --no-cache -t ${TARGET}-${T4} -f ${T4}.dockerfile .

.PHONY: exec-validate
exec-validate:
		${DOCKER} run ${DKRENVS} ${DKRSRCS} ${TARGET}-${T4}

.PHONY: clean
clean: clean-proto clean-validate clean-catalog clean-playgen

.PHONY: all
all: catalog playgen
