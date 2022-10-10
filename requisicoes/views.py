from django.shortcuts import render
from django.conf import settings
from appconfig import app, host
from datetime import date, datetime
from django.http import JsonResponse

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

def api(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)