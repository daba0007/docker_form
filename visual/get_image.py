#!/usr/bin/env python
# coding:utf-8

import docker
import os
import django
import sys
import re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR,])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker_form.settings")
django.setup()
from visual.models import Image

def docker_image():                 #获取镜像信息
    client = docker.from_env()
    image_id=[]                     # 获取镜像id
    image_repository=[]             # 获取镜像标签
    image_tag=[]                    # 获取镜像版本信息
    image_created=[]                # 获取镜像创建时间
    image_size=[]                   # 获取镜像大小

    imagelist=[]                    # 镜像列表
    for image  in client.images():
        id=re.split(r'(:)',image.get("Id"))[2][0:12]    # 提取id并加工为短id
        image_id.append(id)
        created = re.split(r'[T\.]', client.inspect_image(resource_id=id).get("Created"))[0] + " " + \
                  re.split(r'[T\.]', client.inspect_image(resource_id=id).get("Created"))[1]  # 提取创建时间并加工为时间格式
        image_created.append(created)                   # 去掉".",得到时间b[0]
        image_size.append(image.get("VirtualSize"))
        repository = re.split('[\'\[\]\: ]', image.get("RepoTags")[0])  # 去掉"[" "`" "]" ":",使a变成repo和tag两个字符串
        image_repository.append(repository[0])
        image_tag.append(repository[1])
    i=0
    for image in client.images():
        imagelist.append(Image(id=image_id[i],repository=image_repository[i],tag=image_tag[i],created=image_created[i],size=image_size[i]))
        i+=1
    return imagelist

def docker_search(repository,image,tag):                # 搜索镜像
    client = docker.from_env()
    if "\." in repository:
        search_image=re.split("\.",image)[0]+"-"+image
        if client.search(repository+":"+search_image+":"+tag):
            return 1
        else:
            return ""

def docker_pull(repository,image,tag):                  # 从源拉取镜像
    if docker_search(repository=repository,image=image,tag=tag):
        if tag == "" :
            tag = "latest"
        if repository == "":
            repository = "daocloud.io"
        client = docker.from_env()
        if client.images(repository+"/"+image+":"+tag):
            message="镜像已存在"
        else:
            client.pull(repository=repository+"/"+image,tag=tag)
            message="镜像已获取"
        return message
    else:
        message="镜像不存在"
        return message

def docker_rmi(idlist):                                  # 删除镜像
    client = docker.from_env()
    list = docker_image()
    for id in idlist:
        for ima in list:
            if ima.id==id:
                name=ima.repository+":"+ima.tag
                client.remove_image(name)
    return "success"

def docker_commit(id,reponame,tag):                       # 根据容器生成镜像
    client = docker.from_env()
    client.commit(resource_id=id,repository=reponame,tag=tag)
    return "success"

def docker_build(reponame):                                # 根据dockerfile生成镜像
    client = docker.from_env()
    client.build(path="file/", tag=reponame, rm=True)
    return "success"