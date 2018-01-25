#!/usr/bin/env python
# coding:utf-8

from django.db import models
from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseForm, self).__init__(*args, **kwargs)

class LoginForm(BaseForm, django_forms.Form):				# 继承顺序为Loginform<-Baseform<-django_forms.Form，所以参数是FORM需要的参数;
    username = django_fields.CharField(
        min_length=3,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于3个字符", 'max_length': "用户名长度不能大于32个字符"}
    )
    password = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',			# regex,自定制正则表达式
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    rmb = django_fields.IntegerField(required=False)

    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')


class RegisterForm(BaseForm,django_forms.Form):
    username1 = django_fields.CharField(
        min_length=3,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于3个字符", 'max_length': "用户名长度不能大于32个字符"}
    )
    email1 = django_fields.EmailField(error_messages={'required': '邮箱不能为空.', 'invalid': "邮箱格式错误"})
    password1 = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    password2 = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    check_code1 = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def clean_check_code1(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code1').upper():
            raise ValidationError(message='验证码错误!!!', code='invalid')
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次密码输入不一致!!!")
        return password2

class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name = u'用户名',max_length=32,unique = True)
    password = models.CharField(verbose_name=u'密码',max_length=64)
    email = models.EmailField(verbose_name=u'邮箱',unique=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)