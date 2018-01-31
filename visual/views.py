#!/usr/bin/env python
# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from visual.models import Image,Container
from visual.get_image import docker_image,docker_pull,docker_rmi,docker_commit,docker_build
from visual.get_container import docker_ps,docker_create,docker_rm,docker_start,docker_stop,docker_pause,docker_unpause,docker_status
from django.views.decorators.csrf import csrf_exempt
from user.views import check_login
from connect.models import Docker_host
import json
import re
import string

@check_login
def home(request):
    """
    回到主页
    """
    return render(request, 'home.html')

#########################镜像########################################

@check_login
def image(request):
    """
    回到镜像页面
    """
    hostList = Docker_host.objects.all()
    imageip="0.0.0.0"
    return render(request, 'image.html',{'hostList':hostList,'imageip':imageip})

@check_login
def image_table(request):
    """
    得到镜像信息
    """
    imageip="0.0.0.0"
    imagelist = docker_image(imageip)
    rst=[]
    for image in imagelist:
        rst.append({
            "id": image.id,
            "repository": image.repository,
            "tag": image.tag,
            "created": image.created,
            "size": image.size
        })
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def image_newtable(request):
    """
    选择主机得到镜像信息
    """
    imageip=request.POST.get('ip', '')
    imagelist = docker_image(imageip)
    rst=[]
    for image in imagelist:
        rst.append({
            "id": image.id,
            "repository": image.repository,
            "tag": image.tag,
            "created": image.created,
            "size": image.size
        })
    return HttpResponse(json.dumps(rst))

@check_login
def image_add(request):
    """
    增加镜像
    """
    containerlist=docker_ps()
    return render(request, 'image_add.html',{'containerlist':containerlist})

@csrf_exempt
def docker_pull_image(request):
    """
    从镜像源拉取镜像
    """
    image = request.POST.get('image', '')
    if image:
        tag = request.POST.get('tag', '')
        reponame = request.POST.get('reponame', '')
        if "/" in image:                    # 如果用户将容器源填入镜像中，以此填写为主
            reponame=re.split("/",image)[0]
            image=re.split("/",image)[1]
        message=docker_pull(reponame,image,tag)
    else:
        message="请填写镜像"
    rst = {
        "message": message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def image_del(request):
    """
    删除镜像
    """
    idlist=request.POST.getlist('idlist', '')
    repositorylist = request.POST.getlist('repositorylist', '')
    list=docker_ps()
    flag=0
    for repository in repositorylist:
        for con in  list:
            if repository == con.image:      # 首先判断是否存在在使用镜像的容器，存在则提示先删除容器
                flag=1
    if flag == 1:
        message = "存在正在使用的容器，请先删除该容器"
    else:                                    # 若选择的所有镜像都没有使用容器的，则进行删除
        docker_rmi(idlist)
        message = repositorylist[0]+"等镜像已删除"
    rst = {'message': message}
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def image_commit(request):
    """
    基于容器创建镜像
    """
    container = request.POST.get('container', '')
    reponame = request.POST.get('reponame', '')
    tag = request.POST.get('tag', '')
    list=docker_ps()
    for con in list:
        if con.name ==  container:
            id=con.id
    if (tag=="" and reponame):
        tag = "latest"
    docker_commit(id=id,reponame=reponame,tag=tag)
    message="镜像"+reponame+"已生成"
    rst = {
        "message": message
    }
    print(rst)
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def image_dockerfile(request):
    """
    基于dockerfile创建镜像
    """
    reponame = request.POST.get('reponame', '')
    print(reponame)
    file = request.POST.get('file', '')
    if (reponame and file):
        dockerfile = open("file/Dockerfile", 'w')
        dockerfile.write(file)
        dockerfile.close()                      # 得到dockerfile文件
        docker_build(reponame)
        message="镜像已生成"
    else:
        message="请重新填写信息"
    rst = {
        'message': message
    }
    return HttpResponse(json.dumps(rst))

@check_login
def container(request):
    """
    返回容器页面
    """
    hostList = Docker_host.objects.all()
    containerip="0.0.0.0"
    return render(request, 'container.html',{'hostList':hostList,'containerip':containerip})

@check_login
def container_table(request):
    """
    容器信息页面
    """
    conip="0.0.0.0"
    containerlist = docker_ps(conip)
    rst = []
    for container in containerlist:
        rst.append({
            "id": container.id,
            "con_port": container.con_port,
            "name": container.name,
            "created": container.created,
            "status": container.status,
            "image": container.image,
            "command": container.command,
        })
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_newtable(request):
    """
    容器信息页面
    """
    conip=request.POST.get('ip', '')
    containerlist = docker_ps(conip)
    rst = []
    for container in containerlist:
        rst.append("Object"+{
            "id": container.id,
            "con_port": container.con_port,
            "name": container.name,
            "created": container.created,
            "status": container.status,
            "image": container.image,
            "command": container.command,
        },)
    return HttpResponse(json.dumps(rst))

@check_login
def container_add(request):
    """
    增加容器页面
    """

    containerlist=docker_ps()
    return render(request, 'container_add.html',{'containerlist':containerlist})

@csrf_exempt
def docker_create_container(request):
    """
    通过镜像创建容器
    """

    image = request.POST.get('container', '')
    if image:                               # 如果镜像有填写，则运行，否则警告增加镜像
        tag = request.POST.get('tag', '')
        if tag == "":                       # 默认版本最新
            tag="latest"
        reponame = request.POST.get('reponame', '')
        if reponame == "":                  # 默认镜像源daocloud.io
            reponame = "daocloud.io"
        if "/" in image:                    # 如果用户将容器源也填入镜像中
            reponame=re.split("/",image)[0]
            image=re.split("/",image)[1]
        command = request.POST.get('command', '')                                                   # 运行命令
        name = request.POST.get('name', '')                                                         # 容器名
        check_d = request.POST.get('check_d', '')                                                   # 守护态
        check_volume = request.POST.get('check_volume', '')                                        # 验证是否设置数据卷
        volume_local_list = request.POST.getlist('volume_local_list[]', '')                       # 数据卷在集群中的名字
        volume_container_list = request.POST.getlist('volume_container_list[]', '')               # 数据卷在容器中的名字
        volume_permission= request.POST.getlist('volume_permission[]', '')                        # 设置数据卷权限
        check_port = request.POST.get('check_port', '')                                            # 验证是否设置端口映射
        port_local_list = request.POST.getlist('port_local_list[]', '')                           # 在主机的端口
        port_container_list = request.POST.getlist('port_container_list[]', '')                   #在容器中的端口
        check_link= request.POST.get('check_link', '')                                             # 验证是否设置连接
        alias_name=request.POST.getlist('alias_name[]', '')                                        # 要连接的容器名
        host_name = request.POST.getlist('host_name[]', '')                                        # 在容器中的名称
        check_volume_from = request.POST.get('check_volume_from', '')                             # 验证是否要建立数据卷容器
        volume_from_select = request.POST.get('volume_from_select', '')                           # 数据卷容器

        message = docker_create(image=image, reponame=reponame, tag=tag, command=command, name=name, detach=check_d,
                                volume_container_list=volume_container_list, volume_local_list=volume_local_list,
                                volume_permission=volume_permission, port_local_list=port_local_list,
                                port_container_list=port_container_list, alias_name=alias_name, host_name=host_name,
                                check_link=check_link, check_port=check_port, check_volume=check_volume,
                                check_volume_from=check_volume_from,volume_from_select=volume_from_select)
    else:
        message="请填写镜像"
    rst = {'message': message}
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_rm(request):
    """
    移除容器
    """

    idlist=request.POST.getlist('idlist', '')
    statuslist = request.POST.getlist('statuslist', '')
    flag = 1
    for status in statuslist:
        if (docker_status(status) == 'exited' or docker_status(status) == 'created'):              # 若容器处于退出或刚创建，可以删除
            flag = 0
    if flag == 1:
        message = "存在正在使用的容器，请先删除该容器"
    else:
        docker_rm(idlist)
        message=idlist[0]+"等容器删除成功"
    rst = {
        "message": message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_start(request):
    """
    启动
    """

    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_start(id=id,status=status)
    rst = {
        'message': message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_stop(request):
    """
    停止
    """

    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_stop(id=id,status=status)
    rst = {'message': message}
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_pause(request):
    """
    暂停容器
    """

    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_pause(id=id,status=status)
    rst = {
        'message': message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_unpause(request):
    """
    继续容器
    """

    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_unpause(id=id,status=status)
    rst = {
        'message': message
    }
    return HttpResponse(json.dumps(rst))