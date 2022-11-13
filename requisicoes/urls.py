# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

app_name = 'requisicoes'
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    path('index/?secao=<secao>&ano=<ano>&nr=<nr>', views.index, name='index'),
    path('login', views.userlogin, name='login'),
    path('logout', views.userlogout, name='logout'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('profile/', views.profile, name='profile'),
    path('conf/', views.conf, name='conf'),
    path('getodt/<str:processo>', views.getodt, name='getodt'),
    path('api/<str:oq>', views.api, name='api'),
    path('api/', views.api, name='api'),
    path('getanos/', views.getanos, name='getanos'),
    path('getcomentarios/<str:processo>', views.getcomentarios, name='getcomentarios'),
    path('pendencias/<str:quem>', views.pendencias, name='pendencias'),
]