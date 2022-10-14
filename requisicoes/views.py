from django.shortcuts import render, redirect
from django.conf import settings
from appconfig import app, host
from datetime import date, datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

def getcomentarios(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

# /requisicoes/default/getanos?secao=S3
"""
def getanos():
    if request.vars.secao:
        rows=dbpg(dbpg.processo_requisitorio.secao_ano_nr.contains(request.vars.secao)).select(dbpg.processo_requisitorio.secao_ano_nr)
    else:
        rows = []
    #duas secoes com nome parecidos pode dar m aqui
    anos=[r.secao_ano_nr.split("_")[-2] for r in rows]
    anos.append(request.now.strftime('%Y'))
    return response.json(sorted(list(set(anos))))
"""

def getanos(request):
    retorno = "n"
    if request.GET.get('anos','') == "1":
        retorno = "anos"
    if request.GET.get('secao',False):
        retorno = request.GET.get('secao')
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG,
        "retorno" : retorno
    } 
    return JsonResponse(context)

def getodt(request,secao):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def index(request):
    retorno = ""
    user = None
    is_logged_in = False
    if request.user.is_authenticated:
        user = request.user
        is_logged_in = True
        retorno = "Usuário existente"
    context = {
        "app": app,
        "ano":"2022",
        "secao":"almox",
        "nr":"01",
        "flash":"",
        "CHANGELOG": settings.CHANGELOG,
        "auth":{"user": user, "is_logged_in": is_logged_in},
        "form_user":"ccc",
        "today": datetime.now().strftime("%d/%m/%Y"),
        "editavel":True,
        "validade":'null',
        "retorno": retorno
    } 
    return render(request, 'requisicoes/index.html', context)

def userlogin(request):
    if request.POST.get('username') and request.POST.get('password'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect('requisicoes:index')

def userlogout(request):
    logout(request)
    return redirect('requisicoes:index')

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

def api(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)