#!/usr/bin/env python
# coding:utf-8

from connect.ansible import ansible_playbook
from connect.models import Docker_host
import json
import os
import datetime

def join_host(uid,ip,user,password,logindate):
    file="/etc/ansible/hosts"
    with open(file, "w") as f:
        f.write("[hosts]\n" + ip)
    os.system("sshpass -p " + password + " ssh-copy-id -o StrictHostKeyChecking=no " + user + "@" + ip)  # 复制公钥到目标主机
    ansible_playbook('connect/playbook/docker.yml')  # 为目标安装docker
    Docker_host.objects.create(uid=uid, ip=ip, user=user, password=password, logindate=logindate)  # 将主机信息加入数据库
    print(ip+"加入成功")