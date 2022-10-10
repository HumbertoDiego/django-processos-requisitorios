# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

app_name = 'requisicoes'
urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.login, name='logout'),
    path('pesquisar/', views.login, name='pesquisar'),
    path('profile/', views.login, name='profile'),
    path('conf/', views.login, name='conf'),
    path('getodt/<str:processo>', views.getodt, name='getodt'),
]