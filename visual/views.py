#!/usr/bin/env python
# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from visual.get_image import docker_image,docker_pull,docker_rmi,docker_commit,docker_build
from visual.get_container import docker_ps,docker_create,docker_rm,docker_start,docker_stop,docker_pause,docker_unpause,docker_status
from django.views.decorators.csrf import csrf_exempt
import json
import re

def home(request):                          # 返回主页
    return render(request, 'home.html')

#########################镜像########################################

def image(request):                         # 返回镜像页面
    return render(request, 'image.html')

def image_table(request):                   # 镜像信息
    imagelist = docker_image()
    #i = 0
    # returnData = {"rows": [],"total": i}  # 当选择服务端上传的时候选择rows上传
    rst=[]
    for image in imagelist:
        #i+=1
        rst.append({
            "id": image.id,
            "repository": image.repository,
            "tag": image.tag,
            "created": image.created,
            "size": image.size
        })
        #returnData['rows'].append({
        #    "id":image.id,
        #    "repository":image.repository,
        #    "tag":image.tag,
        #    "created":image.created,
        #    "size":image.size
        #})
    #returnData['total']=i
    return HttpResponse(json.dumps(rst))

def image_add(request):                     # 增加镜像
    containerlist=docker_ps()
    return render(request, 'image_add.html',{'containerlist':containerlist})

@csrf_exempt
def docker_pull_image(request):             # 从镜像源拉取镜像
    image = request.POST.get('image', '')
    if "/" in image:
        message="镜像填写错误"
    elif image:
        tag = request.POST.get('tag', '')
        reponame = request.POST.get('reponame', '')
        message=docker_pull(reponame,image,tag)
    else:
        message="请填写镜像"
    rst = {
        "message": message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def image_del(request):                      # 删除镜像
    idlist=request.POST.getlist('idlist', '')
    repositorylist = request.POST.getlist('repositorylist', '')
    list=docker_ps()
    flag=0
    for repository in repositorylist:
        for con in  list:
            if repository == con.image:            # 首先判断是否存在在使用镜像的容器，存在则提示先删除容器
                flag=1
    if flag == 1:
        message = "存在正在使用的容器，请先删除该容器"
    else:                                           # 若选择的所有镜像都没有使用容器的，则进行删除
        docker_rmi(idlist)
        message = repositorylist[0]+"等镜像已删除"
    rst = {'message': message}
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def image_commit(request):             # 基于容器创建镜像
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
def image_dockerfile(request):             # 基于容器创建镜像
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
#######################容器#######################################

def container(request):                     # 返回容器页面
    return render(request, 'container.html')

def container_table(request):               # 容器信息页面
    containerlist = docker_ps()
    rst = []
    for container in containerlist:
        # i+=1
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

def container_add(request):                 # 增加容器页面
    return render(request, 'container_add.html')

@csrf_exempt
def docker_create_container(request):       # 通过镜像创建容器
    print(request.POST)
    image = request.POST.get('container', '')
    if "/" in image:
        message="镜像填写错误"
    elif image:                               # 如果镜像有填写，则运行，否则警告增加镜像
        tag = request.POST.get('tag', '')
        if tag == "":                       # 默认版本最新
            tag="latest"
        reponame = request.POST.get('reponame', '')
        if reponame == "":                  # 默认镜像源daocloud.io
            reponame = "daocloud.io"
        command = request.POST.get('command', '')
        name = request.POST.get('name', '')
        check_d = request.POST.get('check_d', '')
        check_volume = request.POST.get('check_volume', '')                                         # 验证是否设置数据卷
        volume_local_list = request.POST.getlist('volume_local_list[]', '')
        volume_container_list = request.POST.getlist('volume_container_list[]', '')
        volume_permission= request.POST.getlist('volume_permission[]', '')                          # 设置数据卷权限
        check_port = request.POST.get('check_port', '')                                             # 验证是否设置端口映射
        port_local_list = request.POST.getlist('port_local_list[]', '')
        port_container_list = request.POST.getlist('port_container_list[]', '')                     #得到端口号和数据卷号之后要进行处理
        check_link= request.POST.get('check_link', '')                                                  # 验证是否设置连接
        alias_name=request.POST.getlist('alias_name[]', '')                                            # 要连接的容器名
        host_name = request.POST.getlist('host_name[]', '')                                            # 在容器中的名称

        message = docker_create(image=image, reponame=reponame, tag=tag, command=command, name=name, detach=check_d,
                                volume_container_list=volume_container_list, volume_local_list=volume_local_list,
                                volume_permission=volume_permission, port_local_list=port_local_list,
                                port_container_list=port_container_list, alias_name=alias_name, host_name=host_name,
                                check_link=check_link, check_port=check_port, check_volume=check_volume)
    else:
        message="请填写镜像"
    rst = {'message': message}
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_rm(request):                      # 移除容器页面
    idlist=request.POST.getlist('idlist', '')
    statuslist = request.POST.getlist('statuslist', '')
    flag = 0
    for status in statuslist:
        if docker_status(status) == 'exited' :  # 首先判断是否存在在使用的容器，存在则提示先停止容器
            flag = 0
        elif docker_status(status) == 'created' :
            flag = 0
        else:
            flag = 1
    if flag == 1:
        message = "存在正在使用的容器，请先删除该容器"
    else:                                       # 若容器都可删除，则进行删除
        docker_rm(idlist)
        message=idlist[0]+"等容器删除成功"
    rst = {
        "message": message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_start(request):                   # 容器开始
    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_start(id=id,status=status)
    rst = {
        'message': message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_stop(request):                   # 容器停止
    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_stop(id=id,status=status)
    rst = {'message': message}
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_pause(request):                   # 容器暂停
    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_pause(id=id,status=status)
    rst = {
        'message': message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def container_unpause(request):                   # 容器继续
    id = request.POST.get('id', '')
    status = request.POST.get('status', '')
    message=docker_unpause(id=id,status=status)
    rst = {
        'message': message
    }
    return HttpResponse(json.dumps(rst))