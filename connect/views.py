#!/usr/bin/env python
# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.views import check_login
from connect.ansible import ansible_playbook
from connect.models import Docker_host,DateEncoder
from connect.host import join_host
import _thread
import json
import re
import os
import datetime

@check_login
def host_in_docker(request):
    """
    进入连接页
    """
    return render(request, 'host_in_docker.html')

@csrf_exempt
def post_docker_hosts(request):
    """
    加入主机
    """
    ip=request.POST.get('ip', '')
    user=request.POST.get('user', '')
    password = request.POST.get('password', '')
    logindate = datetime.datetime.now()
    logindate = logindate.strftime('%Y-%m-%d %H:%M:%S')
    uid = Docker_host.objects.annotate().count()
    while True:                                                                                                     # 防止删除了出现空缺
        if (Docker_host.objects.filter(uid=uid)):
            uid += 1
        else:
            break
    if (Docker_host.objects.filter(ip=ip)):                                                                         # 如果重复加入一台主机，显示主机已加入
        message = "加入主机无效（主机已加入）"
    else:
        try:
            _thread.start_new_thread(join_host,(uid,ip,user,password,logindate,))  # 开启新线程启动
        except :
            message="线程线程失败"
        else:
            message="添加主机线程启动，请等待一段时间后刷新网页 "
    rst = {
        "message": message
    }
    return HttpResponse(json.dumps(rst))

@csrf_exempt
def delete_docker_hosts(request):
    """
    加入主机
    """
    idlist=request.POST.getlist('idlist', '')
    try:
        for id in idlist:
            Docker_host.objects.get(uid=id).delete()
    except:
        message = "删除失败"
    else:
        message = "删除成功"
    rst = {
        "message": message
    }
    return HttpResponse(json.dumps(rst))

@check_login
def get_docker_hosts(request):
    """
    获取主机信息
    """
    Docker_hostList = Docker_host.objects.all()
    rst = []
    for host in Docker_hostList:
        rst.append({
            "uid": host.uid,
            "ip": host.ip,
            "user": host.user,
            "logindate": host.logindate,
        })
    return HttpResponse(json.dumps(rst,cls=DateEncoder))

