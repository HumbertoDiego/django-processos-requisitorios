# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

app_name = 'requisicoes'
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    path('login', views.userlogin, name='login'),
    path('logout', views.userlogout, name='logout'),
    path('pesquisar/', views.login, name='pesquisar'),
    path('profile/', views.login, name='profile'),
    path('conf/', views.login, name='conf'),
    path('getodt/<str:processo>', views.getodt, name='getodt'),
    path('api/<str:oq>', views.api, name='api'),
    path('api/', views.api, name='api'),
    path('getanos/', views.getanos, name='getanos'),
    path('getcomentarios/<str:processo>', views.getcomentarios, name='getcomentarios'),
]