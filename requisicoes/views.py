from django.shortcuts import render
from django.conf import settings
from appconfig import app, host
from datetime import date, datetime

def getodt(request,secao):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def index(request):
    user = {"user":{"username":"capfoo"}}
    context = {
        "app": app,
        "ano":"2022",
        "secao":"almox",
        "nr":"01",
        "flash":"",
        "CHANGELOG": settings.CHANGELOG,
        "auth":{"user":{}, "is_logged_in": False},
        "form_user":"ccc",
        "today": datetime.now().strftime("%d/%m/%Y"),
        "editavel":True,
        "validade":'null'
    } 
    return render(request, 'requisicoes/index.html', context)

def login(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def logout(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def pendencias(request, dequem):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def conf(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def profile(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)