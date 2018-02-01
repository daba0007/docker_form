#!/usr/bin/env python
# coding:utf-8

from django.db import models
import json
import datetime

class Docker_host(models.Model):
    """
    加入docker主机登记信息
    """
    uid = models.IntegerField(verbose_name=u'序号',primary_key=True)
    ip = models.CharField(max_length=100,verbose_name=u'ip地址',null=False,blank=False)
    user = models.CharField(max_length=100,verbose_name=u'用户名',default="")
    password = models.CharField(max_length=100, verbose_name=u'密码', default="")
    logindate = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)

    class Meta:
        verbose_name = u'容器主机'
        verbose_name_plural = verbose_name

class DateEncoder(json.JSONEncoder):
    """
    重写构造json类，遇到日期特殊处理，其余的用内置
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)