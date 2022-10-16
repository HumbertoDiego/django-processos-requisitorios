import re
from urllib import response
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from appconfig import app
from datetime import date, datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from sped.models import Secao, Pessoa, Usuario, Usuario_Pessoa, Usuario_Secao
from .models import Configuracao
import urllib

def get_secoes():
        tempo = 60*60*5
        # em Web2py:PyDAL
        #((dbpgsped.secao.id_pai!=0)&(dbpgsped.secao.in_excluido!="s")).select(dbpgsped.secao.nm_sigla, orderby=dbpgsped.secao.nm_sigla)]
        # em Django
        queryset = Secao.objects.exclude(id_pai=0).exclude(in_excluido="s").values('nm_sigla').order_by('nm_sigla')
        SECOES = [q['nm_sigla'] for q in queryset]
        # Adicionar as seções que mudaram de nome (s3 -> S3) e que possuem algum processo armazenado
        SECOES_PROCESSOS = []
        #[s['secao_ano_nr'].split("_")[0] for s in ]
        #dbpg().select(dbpg.processo_requisitorio.secao_ano_nr)]
        S = sorted(list(set(SECOES+SECOES_PROCESSOS)))
        #t = cache.ram('secoes', lambda: S, time_expire=tempo)
        return S

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

def getSecoesDesteUser(request):
    if request.user.is_authenticated:
        # Web2py:PyDAL way
        #dbpgsped(
        # (dbpgsped.pessoa.nm_login==auth.user.username)&
        # (dbpgsped.pessoa.id_pessoa==dbpgsped.usuario_pessoa.id_pessoa)&
        # (dbpgsped.usuario_pessoa.dt_fim==None) & 
        # (dbpgsped.usuario_pessoa.id_usuario==dbpgsped.usuario_secao.id_usuario) &
        # (dbpgsped.secao.id_secao==dbpgsped.usuario_secao.id_secao))
        # .select(dbpgsped.secao.nm_sigla) #nm_sigla
        # Django way
        secoes = []
        try:
            p = Pessoa.objects.get(nm_login=request.user.username)
        except Pessoa.DoesNotExist:
            return secoes
        u_p = Usuario_Pessoa.objects.filter(dt_fim__isnull=True).filter(id_pessoa=p.id_pessoa)
        for u in u_p:
            try:
                u_s = Usuario_Secao.objects.get(id_usuario=u.id_usuario.id_usuario)
            except Usuario_Secao.DoesNotExist:
                continue
            rows = Secao.objects.filter(id_secao=u_s.id_secao.id_secao)
            secoes.extend([row.nm_sigla for row in rows])
    else:
        secoes = []
    return secoes

def getodt(request,secao):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def my_redirect(url,params):
    response = redirect(url)
    query_string = urllib.parse.urlencode(params)
    response['Location'] += '?' + query_string

############################################### Fim funções de apoio ##########################################

def index(request):
    secoes = get_secoes()
    if request.GET.get('secao_change',False):
        params = dict(secao=request.GET.get('sec',''),ano=request.GET['ano'],nr="01")
        return my_redirect(reverse('requisicoes:index'),params)
    secao = request.GET.get('secao') if request.GET.get('secao') else app['secao_escape']
    ano = request.GET['ano'] if request.GET.get('ano') else date.today().strftime('%Y')
    nr = request.GET['nr'] if request.GET.get('nr') else "01"
    if not request.GET.get('secao') or not request.GET.get('ano') or not request.GET.get('nr'):
        params = dict(secao=secao,ano=ano,nr=nr)
        return my_redirect(reverse('requisicoes:index'),params)
    # Validação das seções
    if secao not in secoes:
        params = dict(secao=secoes[-1],ano=ano,nr=nr)
        return my_redirect(reverse('requisicoes:index'),params)
    # Validação da secao que está sendo editada
    secoesdesteuser = getSecoesDesteUser(request)
    editavel = True if secao in secoesdesteuser else False
    # Validação dos niveis de autorização para este user
    retorno = ""
    user = None
    is_logged_in = False
    if request.user.is_authenticated:
        user = request.user
        is_logged_in = True
        retorno = "Usuário existente"
    #editavel = True if secao in secoesdesteuser else False
    context = {
        "app": app,
        "ano": ano,
        "secao":secao,
        "nr": nr,
        "flash":"",
        "CHANGELOG": settings.CHANGELOG,
        "auth":{"user": user, "is_logged_in": is_logged_in},
        "form_user":"ccc",
        "today": datetime.now().strftime("%d/%m/%Y"),
        "editavel":True,
        "validade":'null',
        "retorno": secao,
        "SECOES": secoes
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