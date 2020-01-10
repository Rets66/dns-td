client = stab-resolver
resolver = full-service-resolver
manager1 = com-manager
manager2 = net-manager
manager3 = org-manager
manager4 = uk-manager
manager5 = info-manager
manager6 = de-manager
port-resolver = 19953
version = 0.1
flag = --privileged

build:
	-docker build --file='Dockerfile/client' --tag='$(client)':'$(version)' .
	-docker build --file='Dockerfile/resolver' --tag='$(resolver)':'$(version)' .
	-docker build --file='Dockerfile/manager' --tag='manager':'$(version)' .

create-net:
	-docker network create --driver=bridge --subnet=172.168.0.0/16 intranet
	-docker network create --driver=bridge --subnet=172.169.0.0/16 global
	-docker network connect global $(resolver)
	-docker network connect intranet manager2

run-container:
	-docker run -itd --name='$(client)' --hostname='$(client)' --net=intranet --ip=172.168.0.2 $(flag) $(client):$(version) /bin/bash
	-docker run -itd --name='$(resolver)' --hostname='$(resolver)' --net=intranet --ip=172.168.0.3 $(flag) $(resolver):$(version) /bin/bash
	#-docker run -itd --name='manager1' --hostname='$(manager1)' --net=global --ip=172.169.0.2  $(flag) manager:$(version) /bin/bash
	-docker run -itd --name='manager2' --hostname='$(manager2)' --net=global --ip=172.169.0.3 $(flag) manager:$(version) /bin/bash

clean:
	-docker network rm intranet p2p manager
	-docker rm -f $(client) $(resovler)
	-docker image rm -f
