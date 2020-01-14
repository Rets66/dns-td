client = stab-r
resolver = full-r
manager1 = com-manager
manager2 = net-manager
manager3 = org-manager
manager4 = uk-manager
manager5 = info-manager
manager6 = de-manager
version = 0.2
flag = --privileged

build:
	-docker build --file='Dockerfile/client' --tag='$(client)':'$(version)' .
	-docker build --file='Dockerfile/resolver' --tag='$(resolver)':'$(version)' .
	-docker build --file='Dockerfile/manager' --tag='manager':'$(version)' .

net:
	-docker network create --driver=bridge --subnet=172.168.0.0/16 intranet
	-docker network create --driver=bridge --subnet=172.169.0.0/16 global

cont:
	-docker run -itd --name='$(client)' --hostname='$(client)' --net=intranet --ip=172.168.0.2 $(flag) $(client):$(version) /bin/bash
	-docker run -itd --name='$(resolver)' --hostname='$(resolver)' --net=intranet --ip=172.168.0.3 $(flag) $(resolver):$(version) /bin/bash
	-docker run -itd --name='manager1' --hostname='$(manager1)' --net=global --ip=172.169.0.3  $(flag) manager:$(version) /bin/bash
	-docker run -itd --name='manager2' --hostname='$(manager2)' --net=global --ip=172.169.0.4 $(flag) manager:$(version) /bin/bash
	-docker run -itd --name='manager3' --hostname='$(manager3)' --net=global --ip=172.169.0.5 $(flag) manager:$(version) /bin/bash
	-docker run -itd --name='manager4' --hostname='$(manager4)' --net=global --ip=172.169.0.6 $(flag) manager:$(version) /bin/bash
	-docker run -itd --name='manager5' --hostname='$(manager5)' --net=global --ip=172.169.0.7 $(flag) manager:$(version) /bin/bash
	-docker run -itd --name='manager6' --hostname='$(manager6)' --net=global --ip=172.169.0.8 $(flag) manager:$(version) /bin/bash
	-docker network connect intranet manager1
	-docker network connect intranet manager2
	-docker network connect intranet manager3
	-docker network connect intranet manager4
	-docker network connect intranet manager5
	-docker network connect intranet manager6
	-docker network connect global $(resolver)

clean:
	-docker rmi -f $(client) $(resolver) $(manager1) $(manager2) $(manager3) $(manager4) $(manager5) $(manager6)
	-docker stop $(client) $(resolver) manager1 manager2 manager3 manager4 manager5 manager6
	-docker rm -f $(client) $(resolver) manager1 manager2 manager3 manager4 manager5 manager6
	-docker network rm intranet global

start:
	-docker start $(client) $(resolver) manager1 manager2 manager3 manager4 manager5 manager6
