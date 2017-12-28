#!/usr/bin/env python
# coding:utf-8

from django.db import models

class Image(models.Model):
    id = models.CharField(max_length=100,verbose_name=u'镜像id',null=False,blank=False,primary_key=True)
    repository = models.CharField(max_length=100,verbose_name=u'镜像标签',default="")
    tag = models.CharField(max_length=10,verbose_name=u'版本',default="")
    created = models.CharField(max_length=50,verbose_name=u'创建时间',default="")
    size =  models.CharField(max_length=50,verbose_name=u'大小',default="")

    class Meta:
        verbose_name = u'镜像管理'
        verbose_name_plural = verbose_name

class Container(models.Model):
    id = models.CharField(max_length=100,verbose_name=u'容器id',null=False,blank=False,primary_key=True)
    con_port = models.CharField(max_length=100,verbose_name=u'容器端口',default="")
    name = models.CharField(max_length=100,verbose_name=u'容器名',default="")
    created = models.CharField(max_length=50,verbose_name=u'创建时间',default="")
    status = models.CharField(max_length=50,verbose_name=u'运行状态',default="")
    image = models.CharField(max_length=50,verbose_name=u'镜像',default="")
    command = models.CharField(max_length=100,verbose_name=u'容器中命令',default="")


    class Meta:
        verbose_name = u'镜像管理'
        verbose_name_plural = verbose_name
