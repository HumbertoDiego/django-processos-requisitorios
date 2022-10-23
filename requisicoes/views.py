from appconfig import app
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.html import mark_safe
from django import forms
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import json
from sped.models import Secao, Pessoa, Usuario, Usuario_Pessoa, Usuario_Secao
from .models import Configuracao, Processo_requisitorio, Anexo, Assinatura
import urllib

def dict2htmltable(data):
    html = ''
    for k,v in data.items():
        html += '<tr>'
        html += '<td><strong>' + k + ':</strong></td>'
        if isinstance(v,str):
            html += '<td>' + v + '</td>'
        elif isinstance(v,dict):
            for k2,v2 in v.items():
                html += '<tr><td></td>'
                html += '<td>' + k2 + ':</td>'
                if isinstance(v2,str):
                    html += '<td>' + v2 + '</td>'
                html += '</tr>'
        elif  isinstance(v,list):
            for y in v:
                html += ''.join('<td>' + y + '</td>' )
        html += '</tr>'
    return mark_safe('<table>' + html + '</table>')


def posto_graduacao(cod_posto_grad, descricao_e_abreviatura=1):
    """Funcao para retornar a abreviatura do posto, a descricao ou ambas.
    Argumentos: 
    Onde: (posto_grad => inteiro que corresponde a um posto ou graduação)
            (descricao_e_abreviatura => inteiro_tipo_dado_retornar => 
                1 para so abreviatura,
                2 para so descrição ou 
                3 para ambos
    """
    abreviatura = ""
    descricao = ""
    #   Exército
    if cod_posto_grad == 1:
        descricao = 'Marechal'
        abreviatura = 'Mar'
    elif cod_posto_grad == 2:
        descricao = 'General de Exército'
        abreviatura = 'Gen Ex'
    elif cod_posto_grad == 3:
        descricao = 'General de Divisão'
        abreviatura = 'Gen Div'
    elif cod_posto_grad == 4:
        descricao = 'General de Brigada'
        abreviatura = 'Gen Bda'
    elif cod_posto_grad == 5:
        descricao = 'Coronel'
        abreviatura = 'Cel'
    elif cod_posto_grad == 6:
        descricao = 'Tenente Coronel'
        abreviatura = 'Ten Cel'
    elif cod_posto_grad == 7:
        descricao = 'Major'
        abreviatura = 'Maj'
    elif cod_posto_grad == 8:
        descricao = 'Capitão'
        abreviatura = 'Cap'
    elif cod_posto_grad == 9:
        descricao = 'Primeiro Tenente'
        abreviatura = '1º Ten'
    elif cod_posto_grad == 10:
        descricao = 'Segundo Tenente'
        abreviatura = '2º Ten'
    elif cod_posto_grad == 11:
        descricao = 'Aspirante a Oficial'
        abreviatura = 'Asp'
    elif cod_posto_grad == 12:
        descricao = 'Subtenente'
        abreviatura = 'S Ten'
    elif cod_posto_grad == 13:
        descricao = 'Primeiro Sargento'
        abreviatura = '1º Sgt'
    elif cod_posto_grad == 14:
        descricao = 'Segundo Sargento'
        abreviatura = '2º Sgt'
    elif cod_posto_grad == 15:
        descricao = 'Terceiro Sargento'
        abreviatura = '3º Sgt'
    elif cod_posto_grad == 16:
        descricao = 'Cabo'
        abreviatura = 'Cb'
    elif cod_posto_grad == 17:
        descricao = 'Soldado'
        abreviatura = 'Sd'
    elif cod_posto_grad == 18:
        descricao = 'Taifeiro Mor'
        abreviatura = 'TM'
    elif cod_posto_grad == 19:
        descricao = 'Taifeiro de Primeira Classe'
        abreviatura = 'T1'
    elif cod_posto_grad == 20:
        descricao = 'Taifeiro de Segunda Classe'
        abreviatura = 'T2'
    elif cod_posto_grad == 21:
        descricao = 'Servidor Civil'
        abreviatura = 'SC'
    elif cod_posto_grad == 22:
        descricao = 'Sem Patente'
        abreviatura = 'SP'
    # Inclusao de Cadete e Aluno
    elif cod_posto_grad == 23:
        descricao = 'Cadete'
        abreviatura = 'Cad'
    elif cod_posto_grad == 24:
        descricao = 'Aluno'
        abreviatura = 'Al'
    #    FAB
    elif cod_posto_grad == 101:
        descricao = 'Marechal do Ar'
        abreviatura = 'Mar'
    elif cod_posto_grad == 102:
        descricao = 'Tenente Brigadeiro'
        abreviatura = 'Ten Brig'
    elif cod_posto_grad == 103:
        descricao = 'Major Brigadeiro'
        abreviatura = 'Maj Brig'
    elif cod_posto_grad == 104:
        descricao = 'Brigadeiro'
        abreviatura = 'Brig'
    elif cod_posto_grad == 105:
        descricao = 'Coronel'
        abreviatura = 'Cel'
    elif cod_posto_grad == 106:
        descricao = 'Tenente Coronel'
        abreviatura = 'Ten Cel'
    elif cod_posto_grad == 107:
        descricao = 'Major'
        abreviatura = 'Maj'
    elif cod_posto_grad == 108:
        descricao = 'Capitao'
        abreviatura = 'Cap'
    elif cod_posto_grad == 109:
        descricao = 'Primeiro Tenente'
        abreviatura = '1º Ten'
    elif cod_posto_grad == 110:
        descricao = 'Segundo Tenente'
        abreviatura = '2º Ten'
    elif cod_posto_grad == 111:
        descricao = 'Aspirante a Oficial'
        abreviatura = 'Asp Of'
    elif cod_posto_grad == 112:
        descricao = 'Cadete'
        abreviatura = 'Cad'
    elif cod_posto_grad == 113:
        descricao = 'Sub-Oficial'
        abreviatura = 'SO'
    elif cod_posto_grad == 114:
        descricao = 'Primeiro Sargento'
        abreviatura = '1S'
    elif cod_posto_grad == 115:
        descricao = 'Segundo Sargento'
        abreviatura = '2S'
    elif cod_posto_grad == 116:
        descricao = 'Terceiro Sargento'
        abreviatura = '3S'
    elif cod_posto_grad == 117:
        descricao = 'Aluno'
        abreviatura = 'Al'
    elif cod_posto_grad == 118:
        descricao = 'Cabo'
        abreviatura = 'Cb'
    elif cod_posto_grad == 119:
        descricao = 'Soldado de Primeira Classe'
        abreviatura = 'S1'
    elif cod_posto_grad == 120:
        descricao = 'Soldado de Segunda Classe'
        abreviatura = 'S2'
    elif cod_posto_grad == 121:
        descricao = 'Taifeiro Mor'
        abreviatura = 'TM'
    elif cod_posto_grad == 122:
        descricao = 'Taifeiro de Primeira Classe'
        abreviatura = 'T1'
    elif cod_posto_grad == 123:
        descricao = 'Taifeiro de Segunda Classe'
        abreviatura = 'T2'
    # Marinha
    elif cod_posto_grad == 201:
        descricao = 'Almirante'
        abreviatura = 'Alte'
    elif cod_posto_grad == 202:
        descricao = 'Almirante-de-Esquadra'
        abreviatura = 'Alte Esq'
    elif cod_posto_grad == 203:
        descricao = 'Vice-Almirante'
        abreviatura = 'V Alte'
    elif cod_posto_grad == 204:
        descricao = 'Contra-Almirante'
        abreviatura = 'C Alte'
    elif cod_posto_grad == 205:
        descricao = 'Capitão-de-Mar-e-Guerra'
        abreviatura = 'CMG'
    elif cod_posto_grad == 206:
        descricao = 'Capitão-de-Mar-e-Guerra Intendente'
        abreviatura = 'CMG(IM)'
    elif cod_posto_grad == 207:
        descricao = 'Capitão-de-Fragata'
        abreviatura = 'CF'
    elif cod_posto_grad == 208:
        descricao = 'Capitão-de-Corveta'
        abreviatura = 'CC'
    elif cod_posto_grad == 209:
        descricao = 'Capitão-Tenente'
        abreviatura = 'CT'
    elif cod_posto_grad == 210:
        descricao = 'Primeiro Tenente'
        abreviatura = '1T'
    elif cod_posto_grad == 211:
        descricao = 'Segundo Tenente'
        abreviatura = '2T'
    elif cod_posto_grad == 212:
        descricao = 'Guarda-Marinha'
        abreviatura = 'GM'
    elif cod_posto_grad == 213:
        descricao = 'Aspirante'
        abreviatura = 'Asp'
    elif cod_posto_grad == 214:
        descricao = 'Suboficial'
        abreviatura = 'SO'
    elif cod_posto_grad == 215:
        descricao = 'Primeiro Sargento'
        abreviatura = '1º SG'
    elif cod_posto_grad == 216:
        descricao = 'Segundo Sargento'
        abreviatura = '2º SG'
    elif cod_posto_grad == 217:
        descricao = 'Terceiro Sargento'
        abreviatura = '3º SG'
    elif cod_posto_grad == 218:
        descricao = 'Cabo'
        abreviatura = 'CB'
    elif cod_posto_grad == 219:
        descricao = 'Soldado(CFN)'
        abreviatura = 'SD'
    elif cod_posto_grad == 220:
        descricao = 'Marinheiro'
        abreviatura = 'MN'

    if descricao_e_abreviatura == 2:
        abreviatura = descricao
    elif descricao_e_abreviatura == 3:
        abreviatura += ' - ' + descricao
    return abreviatura


def get_secoes():
        tempo = 60*60*5
        # em Web2py:PyDAL
        #((dbpgsped.secao.id_pai!=0)&(dbpgsped.secao.in_excluido!="s")).select(dbpgsped.secao.nm_sigla, orderby=dbpgsped.secao.nm_sigla)]
        # em Django
        queryset = Secao.objects.exclude(id_pai=0).exclude(id_pai=None).exclude(in_excluido="s").values('nm_sigla').order_by('nm_sigla')
        SECOES = [q['nm_sigla'] for q in queryset]
        # Adicionar as seções que mudaram de nome (s3 -> S3) e que possuem algum processo armazenado
        SECOES_PROCESSOS = []
        #[s['secao_ano_nr'].split("_")[0] for s in ]
        #dbpg().select(dbpg.processo_requisitorio.secao_ano_nr)]
        S = sorted(list(set(SECOES+SECOES_PROCESSOS)))
        #t = cache.ram('secoes', lambda: S, time_expire=tempo)
        return S if S else ["secoes?"]

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

def getContasDesteUser(request):
    if request.user.is_authenticated:
        # Web2py:PyDAL way
        #dbpgsped(
        # (dbpgsped.pessoa.nm_login==auth.user.username)&
        # (dbpgsped.pessoa.id_pessoa==dbpgsped.usuario_pessoa.id_pessoa)&
        # (dbpgsped.usuario_pessoa.dt_fim==None)&
        # (dbpgsped.usuario_pessoa.id_usuario==dbpgsped.usuario.id_usuario))
        # select(dbpgsped.usuario.id_usuario,dbpgsped.usuario.nm_usuario)
        # Django way
        contas = []
        try:
            p = Pessoa.objects.get(nm_login=request.user.username)
        except Pessoa.DoesNotExist:
            return contas
        u_p = Usuario_Pessoa.objects.filter(dt_fim__isnull=True).filter(id_pessoa=p.id_pessoa)
        for u in u_p:
            try:
                u_s = Usuario_Secao.objects.get(id_usuario=u.id_usuario.id_usuario)
            except Usuario_Secao.DoesNotExist:
                continue
            contas = Usuario.objects.filter(id_usuario=u_s.id_usuario.id_usuario)
        return [(r.id_usuario,r.nm_usuario) for r in contas]
    else:
        return []

def getPrivs(request):
    is_salc,is_fiscal,is_od,is_admin,is_odsubstituto = False,False,False,False,False
    conf = Configuracao.objects.latest('id')
    if not conf:
        try:
            if int(app['conta_admin'][1]) in [r[0] for r in getContasDesteUser(request)]:
                is_admin=True
        except:
            pass
        return is_salc,is_fiscal,is_od,is_admin,is_odsubstituto
    for contadesteuser in getContasDesteUser(request):
        for id_usuario in conf.contas_salc:
            if id_usuario==contadesteuser[0]:
                is_salc=True
        if conf.conta_fiscal==contadesteuser[0]:
            is_fiscal=True
        if conf.conta_od==contadesteuser[0]:
            is_od=True
        if conf.conta_odsubstituto==contadesteuser[0]:
            is_odsubstituto=True
        try:
            if int(list(app['conta_admin'])[1])==contadesteuser[0]:
                is_admin=True
        except:
            pass
    return is_salc,is_fiscal,is_od,is_admin,is_odsubstituto


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
    return response

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
    is_salc,is_fiscal,is_od,is_admin,is_odsubstituto = getPrivs(request)
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
        "editavel":editavel,
        "is_salc":is_salc,
        "is_admin":is_admin,
        "is_od":is_od,
        "is_fiscal":is_fiscal,
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

def pendencias(request, quem):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)

def conf(request):
    # Nem continuar caso não logado
    if request.user.is_authenticated:
        user = request.user
        is_logged_in = True
    else:
        user = None
        is_logged_in = False
        return HttpResponseRedirect('/index/')
    # Sempre necessário
    retorno = ""
    flash = 'Por Favor, preencha o formulário!'
    choices = Usuario.objects.exclude(in_excluido="s").values("id_usuario","nm_usuario")
    choices_list = [('','--------')]
    choices_list.extend([(x['id_usuario'],x['nm_usuario']) for x in choices])
    # TODO estilizar formulário
    class ConfForm(forms.ModelForm):
        class Meta:
            model = Configuracao
            fields = ['contas_salc', 'conta_fiscal', 'conta_od', 'conta_odsubstituto']
        def __init__(self, *args, **kwargs):
            super(ConfForm, self).__init__(*args, **kwargs)
            self.fields['conta_fiscal'] = forms.ChoiceField(choices=choices_list,
                                                            help_text=self.fields['conta_fiscal'].help_text
                                                            )
            self.fields['conta_od'] = forms.ChoiceField(choices=choices_list,
                                                        help_text=self.fields['conta_od'].help_text
                                                        )
            self.fields['conta_odsubstituto'] = forms.ChoiceField(choices=choices_list,
                                                                    help_text=self.fields['conta_odsubstituto'].help_text
                                                                )
            choices_list.pop(0)
            self.fields['contas_salc'] = forms.MultipleChoiceField(choices=choices_list, 
                                                                    widget=forms.CheckboxSelectMultiple,
                                                                    help_text=self.fields['contas_salc'].help_text
                                                                    )
    record = Configuracao.objects.all().order_by('id').last()
    if request.method == 'POST':
        form = ConfForm(request.POST,instance=record)
        if form.is_valid():
            form.save()
            flash = 'Edições salvas!'
            return HttpResponseRedirect('/conf/')
        else:
            flash = 'Formulário tem erros!'
    else:
        # Converter o texto de contas_salc em opções de id
        form = ConfForm(instance=record,
                        initial={
                                 "contas_salc": [int(i) for i in eval(record.contas_salc)]
                                }
                        )
    contasdesteuser = getContasDesteUser(request)
    is_salc,is_admin = False,False
    for contadesteuser in contasdesteuser:
        if record:
            for id_usuario in record.contas_salc:
                if id_usuario==contadesteuser[0]:
                    is_salc=True
                    break
        try:
            if int(app['conta_admin'][1])==contadesteuser[0]:
                is_admin=True
        except:
            pass
    if not (is_admin or is_salc): return HttpResponse(status=403)
    # TODO costruir a página de erro 403
    secoes = get_secoes()
    s_c = []
    for s in secoes:
        s_c.append([s, Processo_requisitorio.objects.filter(secao_ano_nr__icontains=s).count()] )
    context = {
        "flash": flash,
        "CHANGELOG": settings.CHANGELOG,
        "form": form,
        "is_admin": is_admin,
        "is_salc": is_salc,
        "adminuser_id": app['conta_admin'][0] + ": " +str(app['conta_admin'][1]),
        "secoes": s_c,
        "retorno": retorno,
        "auth":{"user": user, "is_logged_in": is_logged_in}
    } 
    return render(request, 'requisicoes/conf.html', context)

def profile(request):
    retorno = ""
    user = None
    is_logged_in = False
    if request.user.is_authenticated:
        user = request.user
        is_logged_in = True
        retorno = "Usuário existente"
    #else: Tirar esse cara daqui   
    contasdesteuser = getContasDesteUser(request)
    is_salc,is_fiscal,is_od,is_admin,is_odsubstituto = getPrivs(request)
    salc,fiscal,od,admin,odsubstituto = ["Sim" if f else "Não" for f in [is_salc,is_fiscal,is_od,is_admin,is_odsubstituto]]
    logado = request.user
    try:
        #pessoa = dbpgsped(dbpgsped.pessoa.nm_login==auth.user.username).select().first().as_dict()
        pessoa = Pessoa.objects.get(nm_login=request.user.username).__dict__
    except Pessoa.DoesNotExist:
        return contas
    pessoa['patente'] = posto_graduacao(pessoa['cd_patente'], 1)
    usuarios = {}
    usuarios 
    for usuario in contasdesteuser:
        #dbpgsped(
        # (dbpgsped.usuario_pessoa.id_pessoa==pessoa['id_pessoa'])&
        # (dbpgsped.usuario_pessoa.dt_fim==None)).
        # select(dbpgsped.usuario_pessoa.id_usuario):
        usuarios[usuario[0]] = Usuario.objects.get(id_usuario=usuario[0]).__dict__
        #dbpgsped.usuario(usuario.id_usuario).as_dict()
    del pessoa['_state']
    del pessoa['id_pessoa']
    del pessoa['cd_patente']
    contas = {}
    for usuario in usuarios:
        s = Usuario_Secao.objects.get(id_usuario=usuarios[usuario]['id_usuario']).id_secao.id_secao
        # dbpgsped(
        # dbpgsped.usuario_secao.id_usuario==usuarios[usuario]['id_usuario'])
        # .select().first().id_secao
        sr = Secao.objects.get(id_secao=s)
        # dbpgsped.secao(s).as_dict()
        contas[usuarios[usuario]['nm_usuario']] = "Seção: "+sr.nm_sigla
    #editavel = True if secao in secoesdesteuser else False
    perfil = {'Contas':contas, 'Pessoa':pessoa, 'Privilégios':{"Admin":admin,"OD":od,"Fiscal":fiscal,"Salc":salc,"OD Substituto":odsubstituto}}
    context = {
        "app": app,
        "flash":"",
        "CHANGELOG": settings.CHANGELOG,
        "auth":{"user": user, "is_logged_in": is_logged_in},
        "form_user":"ccc",
        "today": datetime.now().strftime("%d/%m/%Y"),
        "editavel":True,
        "is_salc":is_salc,
        "is_admin":is_admin,
        "is_od":is_od,
        "is_fiscal":is_fiscal,
        "perfil":dict2htmltable(perfil)
    } 
    return render(request, 'requisicoes/profile.html', context)

def api(request):
    context = {
        "flash":"",
        "CHANGELOG": settings.CHANGELOG
    } 
    return render(request, 'requisicoes/index.html', context)