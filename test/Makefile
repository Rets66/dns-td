client = stab-resolver
resolver = full-service-resolver
port-resolver = 19953
version = 0.1
flag = --privileged

build:
	-docker build --file='Dockerfile/client' --tag='$(client)':'$(version)' .
	-docker build --file='Dockerfile/resolver' --tag='$(resolver)':'$(version)' .

create-net:
	-docker network create --driver=bridge --subnet=172.168.0.0/16 intranet
	-docker network create --driver=bridge --subnet=172.169.0.0/16 p2p
	-docker network create --driver=bridge --subnet=172.170.0.0/16 manager

run-container:
	-docker run -itd --name='$(client)' --hostname='$(client)' --net=intranet $(flag) $(client):$(version) /bin/bash
	-docker run -itd --name='$(resolver)' --hostname='$(resolver)' --net=intranet --link="$(client)" $(flag) $(resolver):$(version) /bin/bash
	#-docker run -itd --name='$(resolver)' --hostname='$(resolver)' --net=intranet --expose=':$(port-resolver)/udp' $(flag) $(resolver):$(version) /bin/bash
#	docker rn -itd --name=

clean:
	-docker network rm intranet p2p manager
	-docker rm -f $(client) $(resovler)
	-docker image rm -f
