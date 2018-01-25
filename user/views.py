#!/usr/bin/env python
# coding:utf-8

from io import BytesIO
from user.models import LoginForm,RegisterForm,UserInfo
from user.check_code import create_validate_code
from django.shortcuts import HttpResponse,redirect,render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import datetime

def check_login(func):
    """
    检查是否可以登入页面，
    验证session和cookie一致则进入，
    不一致则进入登陆页面，
    这是个修饰器，以函数为参数
    """
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return inner


def login(request):
    """
    登陆表格提交
    """
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info =UserInfo.objects. \
                filter(username=username, password=password). \
                values('nid',
                       'username', 'email'
                       ).first()

            if not user_info:
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                request.session['username'] = username
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)  # 设置有限时长
        else:
            print(form.errors)
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))

def register(request):
    """
    注册表格提交
    """
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == 'POST':
        form = RegisterForm(request=request, data=request.POST)
        r1 = form.is_valid()

        if r1:
            print('obj.cleaned_data:', form.cleaned_data)
            username = form.cleaned_data['username1']
            email = form.cleaned_data['email1']
            password = form.cleaned_data['password1']
            create_time = datetime.datetime.now()
            create_time = create_time.strftime('%Y-%m-%d %H:%M:%S')
            print('create_time:', create_time)
            UserInfo.objects.create(username=username, password=password, email=email, create_time=create_time)
            return HttpResponse('regist success!!!')

        else:
            print(form.errors)
            return render(request, 'register.html', {'form': form})

def check_code(request):
    """
    检查验证码
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream,'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

def logout(request):
    """
    登出
    """
    request.session.clear()
    return redirect('/login')