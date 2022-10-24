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

stylelist = ['古风', '油画', '未来主义', '像素风格', '概念艺术', '赛博朋克', '蒸汽波艺术', '像素风格', '写实风格']


@login_required
def index(request):
    return render(request, 'index.html')


def user_login(request):
    script = 'parent.location.reload();'
    if request.user.is_authenticated:
        return render(request, 'index.html', {'scripts': script})
    else:
        if request.method == 'GET':
            return render(request, 'login.html')
        elif request.method == 'POST':
            username = request.POST.get("username")  # Recept the POST and return the data
            password = request.POST.get("pwd")
            info = {'username': username, 'pwd': password}
            print(username, password)
            error_msg = ''
            if username == '':
                error_msg = 'Please Enter the Username.'
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    remembered = info.get(
                        'remembered')  # Implement remember password : if user checked 'remember password'
                    if remembered == 'on':
                        request.session.set_expiry(60 * 60 * 24 * 10)  # Stay the status in 10 days
                    return render(request, 'index.html', {'scripts': script})
                else:
                    error_msg = 'Username or Password Error！'
                    return render(request, 'login.html', {'error_msg': error_msg, 'info': info, 'scripts': ''})
            return render(request, 'login.html', {'error_msg': error_msg, 'info': info, 'scripts': ''})


def register(request):
    script = 'parent.location.reload();'
    if request.method == 'POST':
        # Recept the POST
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        info = {'username': username, 'pwd': password, 'email': email}

        error_msg = ''
        if username == '':
            error_msg = 'Please type the right username!'
        else:
            if User.objects.filter(username=username).exists() != False:
                error_msg = 'User has exists!'
            else:
                if password == '':
                    error_msg = 'Please type the right password!'
                else:
                    # jump to register
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = 1
                    user.save()
                    # jump to log in
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    # redirect to the new url
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
        return render(request, "wenxin.html", context={'rst': rst, 'stylelist': stylelist})
