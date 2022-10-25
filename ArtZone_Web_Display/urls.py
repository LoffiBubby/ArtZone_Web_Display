"""ArtZone_Web_Display URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Art_Zone_App import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', views.index),
    # path('menu/', views.menu),
    path('wenxinpage/', views.WenxinPage),
    path('wenxinapi/', views.WenxinAPI),
    path('wenxinqapage/', views.WenxinQAPage),
    # path('googletranspage/', views.Google_Trans_page),
    # path('googletranslate/', views.Google_Trans),
    path('wenxinqaapi/', views.WenxinQA),
    path('login/', views.user_login),
    path('register/', views.register),
    path('logout/', views.user_logout),
]
