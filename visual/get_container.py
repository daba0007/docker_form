#!/usr/bin/env python
# coding:utf-8

import docker
import os
import django
import sys
import re
from visual.get_image import docker_image,docker_pull,docker_search
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR,])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker_form.settings")
django.setup()
from visual.models import Container

##############判断合法与否#######################
def judge_volume(check_volume,volume_local_list,volume_container_list):
    """
    判断容器卷是否合法,容器卷不存在时永远为真
    """
    judge=1                                                                             # 合法
    if check_volume:                                                                    #如果容器卷存在，不能同时为空
        for i in range(len(volume_local_list)):
            if (volume_local_list[i-1]=="" and volume_container_list[i-1]==""):        # 同时为空不合法
                judge=""
    return judge

def judge_port(check_port,port_local_list,port_container_list):
    """
    判断端口映射是否合法,端口映射不存在时永远为真
    """

    judge=1                                                                             # 合法
    if check_port:                                                                      #如果端口存在，有一个为空报错
        for i in range(len(port_local_list)):
            if (port_local_list[i-1]=="" or port_container_list[i-1]==""):              # 为空不合法
                judge=""
    return judge

def judge_link(check_link,alias_name,host_name):
    """
    判断网络连接是否合法,网络连接不存在时永远为真
    """

    judge=1                                                                             # 合法
    if check_link:                                                                      #如果网络连接存在，有一个为空报错
        for i in range(len(host_name)):
            if (alias_name[i-1]=="" or host_name[i-1]==""):                             # 为空不合法
                judge=""
    return judge

def judge_name(name):
    """
    判断是否存在相同名字的容器
    """

    judge=1
    list = docker_ps()
    for con in list:
        if con.name == name:                                                             # 存在相同名字的容器
            judge=""
    return judge

def judge_exist(reponame,image,tag):
    """
    判断镜像是否存在
    """
    exist = docker_search(repository=reponame, image=image,tag=tag)
    if not exist:
        list = docker_image()
        for ima in list:
            if ima.repository == reponame+"/"+image:           # 如果有镜像的名字
                exist=1
    return exist

################容器命令函数##############
def docker_ps(ip):
    """
    显示容器信息
    """
    url=ip+":4789"
    client = docker.Client(base_url=url)
    container_id=[]                                             # 获取容器id
    container_name=[]                                           # 获取容器标签
    container_status=[]                                         # 获取容器状态
    container_created=[]                                        # 获取容器创建时间
    container_port=[]                                           # 获取端口信息
    container_image=[]                                          # 获取容器镜像信息
    container_command=[]                                        # 获取容器中命令
    containerlist=[]                                            # 容器列表
    for container  in client.containers(all=True):             # 得到的信息不一定存在，需要进行判断

        if container.get("Id"):                                 # 获得短id
            id=container.get("Id")[0:12]
        else:
            id=""
        container_id.append(id)

        if client.inspect_container(resource_id=id).get("Created"):  # 得到创建时间
            created = re.split(r'[T\.]', client.inspect_container(resource_id=id).get("Created"))[0] + " " + \
                      re.split(r'[T\.]', client.inspect_container(resource_id=id).get("Created"))[1]  # 提取创建时间并加工为时间格式
        else:
            created=""
        container_created.append(created)

        if container.get("Status"):                             # 得到运行状态
            status= container.get("Status")                     # 得到容器运行状态
        else:
            status=""
        container_status.append(status)

        if container.get("Names"):                              # 得到名称
            name=re.split('/', container.get("Names")[0])[1]     #得到容器名称
        else:
            name=""
        container_name.append(name)

        if container.get("Ports"):                              # 得到端口
            info=container.get("Ports")[0]                      # 得到端口信息
            port="%s:%s -> %s/%s" %(info.get("IP"),info.get("PrivatePort"),info.get("PublicPort"),info.get("Type"))
        else:
            port=""
        container_port.append(port)

        if container.get("Image"):                              # 得到镜像
            image=container.get("Image")
        else:
            image=""
        container_image.append(image)

        if container.get("Command"):                            # 得到命令
            command=container.get("Command")
        else:
            command=""
        container_command.append(command)

    i=0
    for container in client.containers(all=True):
        containerlist.append(Container(id=container_id[i], con_port=container_port[i], name=container_name[i],
                                       created=container_created[i], status=container_status[i],
                                       image=container_image[i], command=container_command[i]))
        i+=1
    return containerlist

def docker_create(ip,image, reponame, tag, command, detach, name, volume_local_list, volume_container_list,
                      volume_permission, port_local_list, port_container_list, check_link, check_volume, check_port,
                      alias_name, host_name, check_volume_from, volume_from_select):
    """
    创建容器
    """


    if not judge_exist(reponame=reponame,image=image,tag=tag):              # 镜像不存在
        message="镜像不存在"
    elif not judge_name(name):                                              # 定义的容器名不合法
        message="容器名不合法"
    elif not judge_volume(check_volume=check_volume,volume_local_list=volume_local_list,volume_container_list=volume_container_list):# 容器卷不合法
        message="容器卷不合法"
    elif not judge_port(check_port=check_port,port_local_list=port_local_list,port_container_list=port_container_list):             # 端口映射不合法
        message="端口映射不合法"
    elif not judge_link(check_link=check_link,alias_name=alias_name,host_name=host_name):                                           # 网络连接不合法
        message = "网络连接不合法"
    else:                                                                    # 都合法
        url = ip + ":4789"
        client = docker.Client(base_url=url)
        docker_pull(ip=ip,repository=reponame, image=image, tag=tag)          # 拉取镜像
        imagename = "%s/%s:%s" % (reponame, image, tag)                      # 定义镜像名，守护态-d=false
        if detach == "1":                                                     # 设置detach
            flag = False
        else:
            flag = True

        binds = []                                                              # 数据卷数组
        for num in range(len(volume_local_list)):  # 格式container_id = cli.create_container('busybox', 'ls', volumes=['/mnt/vol1', '/mnt/vol2'],host_config=cli.create_host_config(binds=['/home/user1/:/mnt/vol2','/var/www:/mnt/vol1:ro',]))
            binds.append("%s:%s:%s" % (volume_local_list[num - 1], volume_container_list[num - 1],volume_permission[num-1]))       # host_config =client.create_host_config(binds=binds)

        port_bindings = {}                                                     # 端口字典
        for num in range(len(port_local_list)):  # 格式container_id = cli.create_container('busybox', 'ls', ports=[1111, 2222],host_config=cli.create_host_config(port_bindings={1111: 4567,2222: None}))
            port_bindings[port_container_list[num - 1]] = port_local_list[num - 1]                                                  # host_config=  client.create_host_config(port_bindings=port_bindings)

        volume_from_select_list=[]
        volume_from_select_list.append(volume_from_select_list)               # 创建数据卷容器数组
        if not check_volume:
            binds=[]
        if not check_port:
            port_bindings={}
        if not check_volume_from:
            volume_from_select=""
        if not check_link:                                                   # 转换格式，binds是[],port_bindings是{}，volumes_from 和links是""
            links=""
<<<<<<< HEAD
        else:
            links=""                                                          # 暂未开发

=======
>>>>>>> 8f255ff9ef9db31d78985a6ef8c059ce7e9dd799
        host_config = client.create_host_config(binds=binds, port_bindings=port_bindings, links=links,
                                                volumes_from=volume_from_select)                                                     # 设置容器配置
        info = client.create_container(image=imagename, command=command, detach=flag, name=name,
                                      volumes=volume_container_list, ports=port_container_list,
                                      host_config=host_config)                                                                       # 创建容器

        id = "%s" % (info.get("Id")[0:12])
        if detach == "1":
            client.start(resource_id=id)
        message = "容器" + id + "创建成功"
    return message

def docker_status(status):
    """
    容器状态判断函数，up表示运行中，created表示刚创建未运行，exited表示已退出,paused表示暂停
    """

    flag=""
    if "Up" in status:
        flag="up"
    if "Created" in status:
        flag="created"
    if "Paused" in status:
        flag="paused"
    if "Exited" in status:
        flag="exited"
    return flag

def docker_rm(ip,idlist):
    """
    容器删除
    """
    url = ip + ":4789"
    client = docker.Client(base_url=url)
    for id in idlist:
        client.remove_container(resource_id=id)
    return "success"

def docker_start(ip,id,status):
    """
    容器开启
    """
    url = ip + ":4789"
    client = docker.Client(base_url=url)
    flag=docker_status(status)
    if (flag == "exited" or flag== "created"):                         # 若容器处于退出或刚创建，可以开始
        client.start(resource_id=id)
        message=id+"启动成功"
    else:
        message="请确认容器是否处于退出（exited)或刚创建(created）状态"
    return message

def docker_stop(ip,id,status):
    """
    容器暂停
    """
    url = ip + ":4789"
    client = docker.Client(base_url=url)
    flag = docker_status(status)
    url = ip + ":4789"
    if flag == "up":                                                      # 若容器处于运行，可以关闭
        client.stop(resource_id=id)
        message=id+"退出成功"
    elif flag == "exited":                                               # 若容器处于退出，提示不用关闭
        message = "容器已经处于退出状态"
    else:
        message="请确保容器处于运行（UP）状态"
    return message

def docker_pause(ip,id,status):
    """
    容器暂停
    """
    url = ip + ":4789"
    client = docker.Client(base_url=url)
    flag = docker_status(status)
    if flag == "up" :                                                     # 容器处于运行才可关闭
        client.pause(resource_id=id)
        message=id+"暂停成功"
    else:
        message="请确认容器是否处于开启（Up）状态"
    return message

def docker_unpause(ip,id,status):
    """
    容器开启
    """
    url = ip + ":4789"
    client = docker.Client(base_url=url)
    flag = docker_status(status)
    if flag == "paused" :                                                # 容器处于暂停才可继续
        client.unpause(resource_id=id)
        message=id+"继续运行"
    else:
        message="请确认容器是否处于暂停（Paused）状态"
    return message

