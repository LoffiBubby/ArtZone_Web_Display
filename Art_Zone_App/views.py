from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
import os
import jieba
# -*- coding: utf-8 -*

import wenxin_api
from wenxin_api.tasks.text_to_image import TextToImage


def index(request):
    return render(request, 'index.html')


@login_required
def menu(request):
    return render(request, 'menu.html')


def user_login(request):
    script = 'parent.location.reload();'
    if request.user.is_authenticated:
        return render(request, 'menu.html', {'scripts': script})
    else:
        if request.method == 'GET':
            return render(request, 'login.html')
        elif request.method == 'POST':
            username = request.POST.get("username")  # 接收表单数据，进行登录认证
            password = request.POST.get("pwd")
            info = {'username': username, 'pwd': password}
            print(username, password)
            error_msg = ''
            if username == '':
                error_msg = '请您输入用户名'
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    remembered = info.get('remembered')  # 实现记住密码 : 如果用户勾选了'记住密码'
                    if remembered == 'on':
                        request.session.set_expiry(60 * 60 * 24 * 10)  # 设置状态保持10天
                    return render(request, 'index.html', {'scripts': script})
                else:
                    error_msg = '用户名或密码错误！'
                    return render(request, 'login.html', {'error_msg': error_msg, 'info': info, 'scripts': ''})
            return render(request, 'login.html', {'error_msg': error_msg, 'info': info, 'scripts': ''})


def register(request):
    script = 'parent.location.reload();'
    if request.method == 'POST':
        # 接收表单数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        info = {'username': username, 'pwd': password, 'email': email}
        # 判断数据是否正确
        error_msg = ''
        if username == '':
            error_msg = '错误提示：请您输入用户名'
        else:
            if User.objects.filter(username=username).exists() != False:
                error_msg = '错误提示：该用户已存在'
            else:
                if password == '':
                    error_msg = '错误提示：请输入密码'
                else:
                    # 注册
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = 1
                    user.save()
                    # 登录
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    # 重定向跳转
                    return render(request, 'index.html', {'scripts': script})
        return render(request, 'register.html', {'error_msg': error_msg, 'info': info})
    return render(request, 'register.html')


# 注销
def user_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect('/index/')


def WenxinPage(request):
    return render(request, "wenxin.html")


def WenxinAPI(request):
    if request.method == 'POST':
        wenxin_api.ak = "3eXGhFnSbDr1WEgjSfGGNxoTGjAjitCu"
        wenxin_api.sk = "jhLloOHA7W2E9vczYyBwpxVVDMwLGMmk"
        text = request.POST.get("text")
        style = request.POST.get("style")
        resolution = request.POST.get("resolution")
        input_dict = {
            "text": text,
            "style": style,
            "resolution": resolution
        }
        rst = TextToImage.create(**input_dict)
        print(rst["imgUrls"])
        return render(request, "wenxin.html", {'rst': rst})
