#!/usr/bin/python

import docker

def dockerfile_build():
    client=docker.from_env()
    for line in client.pull(repository="daocloud.io/ubuntu",tag="latest"):
        print (line)

dockerfile_build()
