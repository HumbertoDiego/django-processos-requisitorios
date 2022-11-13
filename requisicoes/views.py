from appconfig import app, sped, ldap as ldapconf
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.utils.html import mark_safe
from django import forms
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
import json
from sped.models import Secao, Pessoa, Usuario, Usuario_Pessoa, Usuario_Secao
from .models import Configuracao, Processo_requisitorio, Anexo, Assinatura, Comentario
import urllib
from django.views.decorators.csrf import csrf_exempt
import re
from django.db.models import Q
import os

######## Funções de apoio
 
def CRYPT(text, key="", salt="", digest_alg="sha256"):
    """Generate hash with the given text using the specified digest algorithm."""
    import hmac
    text = text.encode("utf-8", "strict")
    key = key.encode("utf-8", "strict")
    salt = salt.encode("utf-8", "strict")
    h = hmac.new(key + salt, text, digest_alg)
    hashed = h.hexdigest()
    crypted = "%s$%s$%s" % (digest_alg, salt.decode(), hashed)
    return crypted

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
        return S if S else ["???"]

def my_redirect(url,params):
    response = redirect(url)
    query_string = urllib.parse.urlencode(params)
    response['Location'] += '?' + query_string
    return response

#########
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

def getcomentarios(request,processo):
    rows=Comentario.objects.filter(pr__iexact=processo)
    retorno = []
    for row in rows:
        retorno.append({"autor":row.autor,"comentario":row.comentario,"datahora":row.datahora.strftime("%d-%m-%Y %H:%M:%S")})
    return JsonResponse(retorno, safe=False)

def getPrivs(request):
    is_salc,is_fiscal,is_od,is_admin,is_odsubstituto = False,False,False,False,False
    try:
        conf = Configuracao.objects.latest('id')
    except:
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

def getodt(request,processo):
    def teste_encoding(a):
        if hasattr(a, 'decode'): return a.decode("utf-8")
        else: return a
    processo = urllib.parse.unquote(processo)
    try:
        row = Processo_requisitorio.objects.get(secao_ano_nr=processo)
    except:
        return HttpResponse('Bad Request', status=400)
    varsjson = {}
    try:
        dados = json.loads(row.dados)
    except ValueError:
        # query = dbpg.processo_requisitorio.dados.like('%\\x%')
        # os dados devem ter caracteres unicode no formato \u00VV e não \xVV, editar pelo pgadmin4 causa esse bug!!!
        # Solução é encotrar, copiar os dados, substituir no sublime \x por \u00 e atualizar. Se precisar voltar a valdiade para null:
        #UPDATE public.processo_requisitorio SET valido=null WHERE id=1;-- é o modo correto de editar a validade
        dados = json.loads(row.dados.decode("unicode_escape")) # TODO Aprender como converter em Python 2
        #return response.json({"vars":row.dados,"erro":str(e)+str(e.args)})
    try:
        from relatorio.templates.opendocument import Template
        from io import open, BytesIO
        meses = [u"Janeiro", u"Fevereiro", u"Março", u"Abril", u"Maio", u"Junho", u"Julho", u"Agosto", u"Setembro" , u"Outubro", u"Novembro", u"Dezembro"]
        mes_abr = [m[:3] for m in meses]
        fbase = open(os.path.join(settings.BASE_DIR,'vars.json'),'r', encoding="utf-8").read()
        varsjson = json.loads(fbase)
        varsjson.update(dados)
        dicmodos = {"gerente":"Gerente/Participante", "carona":"Carona","dispensa":u"Dispensa de Licitação","inex":"Inexigibilidade"}
        for quem in ["requisitante","fiscal","od"]:
            for modo in ["gerente", "carona","dispensa","inex","anul"]:
                for doc in ["pr","pedido","comparativo","justificativa","etp"]:
                    if "ass_"+quem+"_"+doc+"_"+modo not in varsjson:
                        varsjson["ass_"+quem+"_"+doc+"_"+modo] = ""
        varsjson['hash']=str(CRYPT(row.dados))
        try:
            varsjson['secao']=processo.split("_")[0]
            varsjson['ano']=processo.split("_")[1]
            varsjson['nr']=processo.split("_")[2]
        except:
            return HttpResponse('Bad Request', status=400)
        varsjson['dataextenso']= varsjson["data"].split("/")[0] + " de " + meses[int(varsjson["data"].split("/")[1])-1]
        varsjson['dataresumidalower']= teste_encoding(varsjson["data"].split("/")[0]+" "+mes_abr[int(varsjson["data"].split("/")[1])-1])
        varsjson['dataresumidalower']= varsjson['dataresumidalower']
        varsjson['cidadeestado'] = app['orgcidade']+"/"+app['orgestadoabrev']#"Manaus"+"/"+"AM" ##
        varsjson['omextenso'] = app['orgextenso'].upper() #"4º CENTRO DE GEOINFORMAÇÃO"#
        varsjson['omabrev'] = app['orgabrev'] #"4º CGEO"#
        varsjson['omendereco'] = app['orgendereco'] #"Avenida Marechal Bittencourt, nº 97, bairro Santo Antônio, CEP – 69029-160, em Manaus/AM"#
        varsjson['timbre_linha1'] = app['timbre_linha1'] #"MINISTÉRIO DA DEFESA"#
        varsjson['timbre_linha2'] = app['timbre_linha2'] #"EXÉRCITO BRASILEIRO"#
        varsjson['omsup'] = app['timbre_linha3'] #"DCT - DSG"#
        varsjson['objs'] = []
        cp = varsjson.copy()
        for k in cp:
            if "_edited" in k: varsjson.pop(k)
            elif "odsubstituto" in k:
                if varsjson[k]!="":
                    varsjson[k]=varsjson[k]+" "
        qttotaldeitens = []
        for k,v in varsjson.items():
            if "nritem" in k or "catmatitem" in k or "descricaoitem" in k or "qtitens" in k or "valorfornecedor2" in k or "somaparcial" in k :
                qttotaldeitens.append(k.split("-")[1])
        for ordem in sorted(set(qttotaldeitens)):
            varsjson['objs'].append({
                    'nritem':varsjson['nritem-'+ordem].replace("\\n","") if 'nritem-'+ordem in varsjson else "",
                    'descricaoitem':varsjson['descricaoitem-'+ordem] if 'descricaoitem-'+ordem in varsjson else "",
                    'u':varsjson['unidade-'+ordem] if 'unidade-'+ordem in varsjson else "",
                    'unidade':varsjson['unidade-'+ordem] if 'unidade-'+ordem in varsjson else "",
                    'qtitens':varsjson['qtitens-'+ordem] if 'qtitens-'+ordem in varsjson else "",
                    'valor':varsjson['valor-'+ordem] if 'valor-'+ordem in varsjson else "",
                    'catmatitem':varsjson['catmatitem-'+ordem] if 'catmatitem-'+ordem in varsjson else "",
                    'somaparcial':varsjson['somaparcial-'+ordem] if 'somaparcial-'+ordem in varsjson else "",
                    'valorvencedor':varsjson['valorvencedor-'+ordem] if 'valorvencedor-'+ordem in varsjson else "",
                    'valorfornecedor1':varsjson['valorfornecedor1-'+ordem] if 'valorfornecedor1-'+ordem in varsjson else "",
                    'valorfornecedor2':varsjson['valorfornecedor2-'+ordem] if 'valorfornecedor2-'+ordem in varsjson else "",
                    'valorfornecedor3':varsjson['valorfornecedor3-'+ordem] if 'valorfornecedor3-'+ordem in varsjson else "",
                    'valorfornecedor4':varsjson['valorfornecedor4-'+ordem] if 'valorfornecedor4-'+ordem in varsjson else "",
                    'valorcomparacao1':varsjson['valorcomparacao1-'+ordem] if 'valorcomparacao1-'+ordem in varsjson else "",
                    'valorcomparacao2':varsjson['valorcomparacao2-'+ordem] if 'valorcomparacao2-'+ordem in varsjson else "",
                    'valorcomparacao3':varsjson['valorcomparacao3-'+ordem] if 'valorcomparacao3-'+ordem in varsjson else "",
                    'unit2':varsjson['unit2-'+ordem] if 'unit2-'+ordem in varsjson else "",
                    'unit3':varsjson['unit3-'+ordem] if 'unit3-'+ordem in varsjson else ""
                    })
        modelo = "" if varsjson['modo']=="gerente" else "_dispensa" if varsjson['modo']=="dispensa" else "_anul" if varsjson['modo']=="anul" else "_carona"
        varsjson['aquisicaopor'] = dicmodos.get(varsjson['modo'],"Gerente") if varsjson['modo']!="gerente" else u"Pregão "+varsjson['gerpar']
        ## SolUÇÃO para: "'ascii' codec can't decode byte 0xc3 in position 9: ordinal not in range(128)"
        # varsjson["key"] = teste_encoding(varsjson["key"])
        filename2=os.path.join(settings.BASE_DIR,'requisicoes','static','modelos','pr'+modelo+'_model.odt')
        basic = Template(source='', filepath=filename2)
        bufferimg = BytesIO()
        bufferimg.write(basic.generate(o=varsjson).render().getvalue())
        bufferimg.seek(0)
        try: 
            response = HttpResponse(bufferimg, content_type='application/vnd.oasis.opendocument.text')
            response['Content-Disposition'] = 'attachment; filename="%s"'%("PR_"+processo+".odt")
        except IOError:
            response = HttpResponseNotFound('<h1>File not exist</h1>')
        return response
    except Exception as e:
        return JsonResponse({"vars":varsjson,"erro":str(e)+str(e.args)})

############################################### Fim funções de apoio ##########################################

def index(request, secao="", ano="", nr=""):
    retorno = ""
    qs = urllib.parse.parse_qs(request.META['QUERY_STRING'])
    if not qs:
        qs = urllib.parse.parse_qs(request.META['PATH_INFO'])
    if not qs:
        qs = request.GET.copy()
    for k, v in qs.items():
        if isinstance(v,list):
            if v:
                qs[k] = v[0]       
    if qs.get('secao_change',False):
        params = dict(secao=qs.get('sec',''),ano=qs.get('ano',''),nr="01")
        return my_redirect(reverse('requisicoes:index'),params)
    secao = qs.get('secao',app['secao_escape'])
    nr = qs.get('nr', "01")
    ano = qs.get('ano', date.today().strftime('%Y'))
    if not qs.get('secao') or not qs.get('ano') or not qs.get('nr'):
        params = dict(secao=secao,ano=ano,nr=nr)
        return my_redirect(reverse('requisicoes:index'),params)
    # Validação das seções
    secoes = get_secoes()
    if secao not in secoes:
        params = dict(secao=secoes[-1],ano=ano,nr=nr)
        return my_redirect(reverse('requisicoes:index'),params)
    # Validação da secao que está sendo editada
    secoesdesteuser = getSecoesDesteUser(request)
    editavel = True if secao in secoesdesteuser else False
    # Validação dos niveis de autorização para este user
    user = None
    is_logged_in = False
    if request.user.is_authenticated:
        user = request.user
        is_logged_in = True
    is_salc,is_fiscal,is_od,is_admin,is_odsubstituto = getPrivs(request)
    rows = Processo_requisitorio.objects.filter(secao_ano_nr__contains=secao+"_"+ano).order_by('-id')
    nr = "01" if not rows else nr
    if not rows: # nenhum lançamento ainda
        hashed = ""
        row = {"dados":""}
        arq_carona = []
        arq_dispensa = []
        arq_inex = []
        validade = None
    else:
        row = Processo_requisitorio.objects.get(secao_ano_nr__contains=secao+"_"+ano+"_"+nr)
        hashed = CRYPT(row.dados)
        # pegar as url dos arquivos
        arq_carona = Anexo.objects.filter(pr__exact=secao+"_"+ano+"_"+nr).filter(modo="carona")
        arq_dispensa = Anexo.objects.filter(pr__exact=secao+"_"+ano+"_"+nr).filter(modo="dispensa")
        arq_inex = Anexo.objects.filter(pr__exact=secao+"_"+ano+"_"+nr).filter(modo="inex")
        validade = row.valido
    context = {
        "app": app,
        "ano": ano,
        "secao": secao,
        "nr": nr,
        "flash": "",
        "CHANGELOG": settings.CHANGELOG,
        "MAXSIZE": settings.MAXSIZE, 
        "ALLOWED": settings.ALLOWED,
        "auth": {"user": user, "is_logged_in": is_logged_in},
        "form_user": "ccc",
        "today": datetime.now().strftime("%d/%m/%Y"),
        "editavel": editavel,
        "is_salc": is_salc,
        "is_admin": is_admin,
        "is_od": is_od,
        "is_fiscal": is_fiscal,
        "validade": 'null',
        "retorno": retorno,
        "SECOES": secoes,
        "rows": rows,
        "row": row,
        "arq_carona": arq_carona,
        "arq_dispensa": arq_dispensa,
        "arq_inex": arq_inex,
        "validade": json.dumps(validade),
        "hashed": hashed
    } 
    return render(request, 'requisicoes/index.html', context)

def pendencias(request, quem):
    quem = quem if quem else "od"
    q =request.GET.get("q","")
    if not q:
         return my_redirect(reverse('requisicoes:pendencias',args=[quem]),dict(q=datetime.now().strftime('%Y')))
    msg = ""
    user = None
    is_logged_in = False
    if request.user.is_authenticated:
        user = request.user
        is_logged_in = True
    is_salc,is_fiscal,is_od,is_admin,is_odsubstituto = getPrivs(request)
    if quem in ["fiscal", "od"]:
        rows = Processo_requisitorio.objects.filter(valido=True).filter(secao_ano_nr__contains=q).order_by('id')
    elif quem in ["requisitante","salc"]:
        rows = Processo_requisitorio.objects.filter(valido=None).filter(secao_ano_nr__contains=q).order_by('id')
    else:
        rows = []
    # Checagem das assinaturas dessas rows
    shows2 = []
    lista_assinaturas = []
    for row in rows:
        mostrar = False
        show={}
        hidden={}
        try:
            dic = json.loads(row.dados)
        except Exception as e:
            s = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', row.dados)
            dic = json.loads(s)
            msg = str(e)+"---- Processo: ("+str(row.id)+") "+str(row.secao_ano_nr)
        modo = dic.get('modo','gerente')
        if quem=="salc": w="requisitante"
        else: w=quem
        if modo == "anul":
            lista_assinaturas = ["ass_"+w+"_pr_"+modo]
        elif modo == "inex":
            lista_assinaturas = ["ass_"+w+"_pr_"+modo,"ass_"+w+"_pedido_"+modo,"ass_"+w+"_justificativa_"+modo,"ass_"+w+"_etp_"+modo]
        elif modo == "dispensa":
            lista_assinaturas = ["ass_"+w+"_pr_"+modo,"ass_"+w+"_pedido_"+modo,"ass_"+w+"_justificativa_"+modo]
        elif modo == "carona":
            lista_assinaturas = ["ass_"+w+"_pr_"+modo,"ass_"+w+"_pedido_"+modo,"ass_"+w+"_justificativa_"+modo, "ass_"+w+"_etp_"+modo]
        elif modo == "gerente":
            lista_assinaturas = ["ass_"+w+"_pr_gerente","ass_"+w+"_pedido_gerente"]
        if quem in ["requisitante","salc"] and modo not in[ "gerente","dispensa"]:
            lista_assinaturas.append("ass_"+w+"_comparativo_"+modo)
        if quem=="salc":
            if all(l in dic for l in lista_assinaturas):
                mostrar = True
        else:
            for l in lista_assinaturas:
                if l not in dic:
                    mostrar = True
                    break
        if mostrar:
            lista_desejados=["data","modo","remetente","beneficios-justificativa"]    
            dados_copy = dic.copy()
            for k,v in dados_copy.items():
                if k in lista_desejados:
                    show[k.upper().replace("_"," ")] = dic.pop(k)
                elif "ass_" in k and "edited" not in k and modo in k:
                    show[k.upper().replace("_"," ")] = dic.pop(k)
            hidden['resumo']=row.resumo
            hidden['ano']=row.secao_ano_nr.split("_")[-2]
            hidden['nr']=row.secao_ano_nr.split("_")[-1]
            hidden['secao']=row.secao_ano_nr.split("_")[0]
            hidden['valido']="Válido" if row.valido==True else "Inválido" if row.valido==False else "Em trabalho"
            beautify_show = dict2htmltable(show)
            shows2.append([beautify_show,hidden])

    context = {
        "msg":msg,
        "CHANGELOG": settings.CHANGELOG,
        "shows":shows2,
        "auth":{"user": user, "is_logged_in": is_logged_in},
        "len_rows": len(shows2),
        "is_salc":is_salc,"is_admin":is_admin,"is_od":is_od,"is_fiscal":is_fiscal,
         "q":"Pendências do(a) "+quem.upper()
    } 
    return render(request, 'requisicoes/pesquisar.html', context)

def pesquisar(request):
    msg = ""
    user = None
    is_logged_in = False
    if request.user.is_authenticated:
        user = request.user
        is_logged_in = True
    is_salc,is_fiscal,is_od,is_admin,is_odsubstituto = getPrivs(request)
    rows =[]
    q = request.GET.get('q',"")
    if q:
        rows = Processo_requisitorio.objects.filter(Q(secao_ano_nr__contains=q) | Q(resumo__contains=q) | Q(dados__contains=q)).order_by('id')
    shows =[]
    for row in rows:
        show={}
        hidden={}
        try:
            dados = json.loads(row.dados)
        except:
            dados = json.loads('{}')
        modo=dados["modo"] if "modo" in dados else "gerente"
        lista_desejados=["data","modo","remetente","beneficios-justificativa"]    
        dados_copy = dados.copy()
        for k,v in dados_copy.items():
            if k in lista_desejados:
                show[k.upper().replace("_"," ")] = dados.pop(k)
            elif "ass_" in k and "edited" not in k and modo in k:
                show[k.upper().replace("_"," ")] = dados.pop(k)
        hidden['resumo']=row.resumo
        hidden['ano']=row.secao_ano_nr.split("_")[-2]
        hidden['nr']=row.secao_ano_nr.split("_")[-1]
        hidden['secao']=row.secao_ano_nr.split("_")[0]
        hidden['valido']="Válido" if row.valido==True else "Inválido" if row.valido==False else "Em trabalho"
    
        beautify_show = dict2htmltable(show)
        shows.append([beautify_show,hidden])
    context = dict(
        auth={"user": user, "is_logged_in": is_logged_in},
        len_rows = len(rows),
        is_salc=is_salc,is_admin=is_admin,is_od=is_od,is_fiscal=is_fiscal,
        q=q,
        msg=msg,
        CHANGELOG=settings.CHANGELOG,
        shows=shows
    )
    return render(request, 'requisicoes/pesquisar.html', context)

def profile(request):
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
    try:
        record = Configuracao.objects.latest('id')
    except:
        record = None    
    if request.method == 'POST':
        form = ConfForm(request.POST,instance=record)
        if form.is_valid():
            form.save()
            flash = 'Edições salvas!'
            #return HttpResponseRedirect('/conf/')
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

@csrf_exempt
def api(request):
    if not request.user.is_authenticated: # somente usuários logados podem usar esta API
        return HttpResponse('Unauthorized', status=401)
    def contas_do_user(user): # reinterpretação de usuarios_da_pessoa(pessoa)
        contas = []
        try:
            p = Pessoa.objects.get(nm_login=user)
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
    secoes_deste_user = getSecoesDesteUser(request)
    def anos_com_processos_desta_secao(secao):
        # Web2py:PyDAL way
        #dbpg(dbpg.processo_requisitorio.secao_ano_nr.contains(secao)).
        # select(dbpg.processo_requisitorio.secao_ano_nr) 
        # duas secoes com nome parecidos pode dar m aqui
        # Django way
        rows = Processo_requisitorio.objects.filter(secao_ano_nr__contains=secao)
        # # "_".join(a.split("_")[:-2]) -> para sempre pegar o nome da secao independe se houver "_" dentro do nome
        anos=[r.secao_ano_nr.split("_")[-2] for r in rows]
        return sorted(list(set(anos)))
    if request.method =='GET':
        dic=dict(anos=False,secoesdesteuser=False)
        vars = request.GET.copy()
        dic['vars'] = vars
        for key, value in dic.items():
            if key in vars: dic.update({key:True if (vars[key] == "1" or vars[key] == "true") else False})
        if dic['anos']:
            try:
                dic['vars'] = vars
                secao = vars.pop('secao')
                dic['anos'] = anos_com_processos_desta_secao(secao)
            except Exception as e:
                return HttpResponse(mark_safe(f'<h2>{e=}</h2>'), status=400)
        if dic['secoesdesteuser']:
            try:
                dic['vars'] = vars
                dic['secoes'] = list(set(secoes_deste_user))
                #dic['processo'] = vars.get('processo',"")#unquote(vars.get('processo',""))
            except Exception as e:
                return HttpResponse(mark_safe(f'<h2>{e=}</h2>'), status=400)
        return JsonResponse(dic)
    elif request.method =='POST':
        dic=dict(novo=False,edit=False,assinar=False,comentar=False,remline=False,up=False)
        dic["del"] = False
        vars = request.POST.copy()
        if not vars:
            vars = json.loads(request.body)
        qs = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        for k, v in qs.items():
            if isinstance(v,list):
                if v:
                    vars[k] = v[0]
            elif isinstance(v,str):
                if v:
                    vars[k] = v
        for key, value in dic.items():
            if key in vars: dic.update({key:True if (vars[key] == ["1"] or vars[key] == "1" or vars[key] == "true") else False})
        #clean data TODO: review this
        vars['processo'] = vars.get('processo',"")
        dic["path"] = request.path
        allowed = list(app['allowed_ext'])
        if dic['novo']:
            try:
                resumo = vars.get('resumo')
                ano = vars.get('ano')
                secao = vars.get('secao')
                groups = secoes_deste_user
                dic['grupos_deste_user'] = groups
            except Exception as e:
                return HttpResponse(mark_safe(f'<h2>{e=}</h2>'), status=400)
            try:
                if secao not in groups:
                    return HttpResponse('Forbidden', status=403)
                else:
                    #web2py
                    # dbpg(dbpg.processo_requisitorio.secao_ano_nr.like(secao+'_'+ano+'%')).select(orderby='id').last()
                    # dbpg.processo_requisitorio.insert( secao_ano_nr=secao+'_'+ano+'_'+nr, resumo=resumo ,dados=response.json({"data":request.now.strftime('%d/%m/%Y'),"modo":"gerente"}))
                    #django
                    try:
                        last = Processo_requisitorio.objects.filter(secao_ano_nr__contains=secao+'_'+ano+'_').latest('id')
                    except:
                        last = None
                    nr = "%02d"%(int(last.secao_ano_nr.split("_")[-1])+1) if last else "01"
                    p = Processo_requisitorio(secao_ano_nr=secao+'_'+ano+'_'+nr, resumo=resumo ,dados=json.dumps({"data":date.today().strftime('%d/%m/%Y'),"modo":"gerente"}))
                    p.save()
                    dic['nr']=nr
                    dic['p'] = p.id
                    params = dict(secao=secao,ano=ano,nr=nr)
                    dic['redirect2'] = '/index?' + urllib.parse.urlencode(params)
                    return JsonResponse(dic)
            except Exception as e:
                return HttpResponse(mark_safe(f'<h2>{e=}</h2>'), status=403)
        if dic['edit']:
            try:
                if vars['processo'].split("_")[0] not in secoes_deste_user: 
                    return HttpResponse(mark_safe('<h2>Usuário não pertence a esta seção.</h2>'), status=403)
                try:
                    pr = Processo_requisitorio.objects.get(secao_ano_nr__contains=vars['processo'])
                except Exception as e:
                    dic['erro'] = str(e)
                    return JsonResponse(dic)
                if pr.valido!=None: 
                    return HttpResponse(mark_safe('<h2>"Este processo já foi encerrado."</h2>'), status=400)
                #1) Proteção contra caracteres mal escapados
                try:
                    dados = json.loads(pr['dados'])
                except Exception as e:
                    s = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', pr.dados)
                    dados = json.loads(s)
                params = dict(secao=vars['processo'].split("_")[0],ano=vars['processo'].split("_")[-2],nr=vars['processo'].split("_")[-1])
                esta_url = '?'+urllib.parse.urlencode(params)
                #2) Acabar com todas as assinaturas
                campos_assinados = [ k for k,v in dados.items() if "ass_" in k]
                for c in campos_assinados:
                    dados.pop(c)
                #3) Adicionar modo
                lista_modos = ["gerente","carona","dispensa","inex","anul"]
                if vars['modo'] in lista_modos and 'modo' not in dados: dados['modo'],dic['redirect2']=vars['modo'],esta_url
                elif vars['modo'] in lista_modos and 'modo' in dados and dados['modo']!=vars['modo']: dados['modo'],dic['redirect2']=vars['modo'],esta_url
                elif vars['modo'] in lista_modos and 'modo' in dados and dados['modo']==vars['modo']: dados['modo']=vars['modo']
                else: dados['modo'],dic['redirect2']="gerente",esta_url
                #4) Edição propriamente dita
                dados[vars['campo']]=re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})' , r'', vars['valor'].replace('"',"'").replace('\n',"\\n"))
                dados[vars['campo']+'_edited']='true'
                pr.dados=json.dumps(dados, sort_keys=True )
                pr.save()
                if campos_assinados:
                    dic['redirect2']=esta_url
                dic['hashed'] = CRYPT(pr.dados)
            except Exception as e:
                msg = f'<div>{e=}<h2></h2><p>{str(pr["dados"])}</p></div>'
                return HttpResponse(mark_safe(msg), status=400)
        if dic['assinar']:
            if 'senha' in vars and 'login' in vars:
                import ldap
                ldap_host = sped.get('host') if sped.get('host') else ldapconf['host']
                l = ldap.initialize('ldap://'+ldap_host)
                username = "cn=%s,%s" % (vars['login'], settings.BASE_DN)
                password = vars['senha']
                try:
                    l.protocol_version = ldap.VERSION3
                    l.simple_bind_s(username, password)
                except Exception as error:
                    return HttpResponse('Unauthorized', status=401)
            else:
                return HttpResponse('Bad Request', status=400)
            # Pegar Post Nome Completo desse login no banco do sped
            try:
                import random,string
            except:
                return HttpResponse('Internal Server Error', status=500)
            try:
                pessoa = Pessoa.objects.get(nm_login__iexact=vars['login']).__dict__
                pessoa['patente'] = posto_graduacao(pessoa['cd_patente'], 1)
                militar = pessoa['patente'] + " " + pessoa['nm_guerra']+ " - "+ pessoa['nm_completo']
            except Exception as e:
                return HttpResponse(str(e), status=500)
            dic['militar']=militar
            # Pegar as contas dessa pessoa
            try:
                contas = contas_do_user(vars['login'])
                dic['contas']=contas
            except:
                return HttpResponse('Internal Server Error', status=500)
            # Comparar o cmapo da assinatura com as autorizações da pessoa que está assinando
            conf = Configuracao.objects.latest('id')
            is_salc = False
            is_fiscal = False
            is_od = False
            is_odsubstituto = False
            odsubstituto = ""
            autorizado = False
            for contadesteuser in contas:
                if conf:
                    for id_usuario in json.loads(conf.contas_salc.replace("'",'"')):
                        if Usuario.objects.get(id_usuario=id_usuario).nm_usuario==contadesteuser[1]:
                            is_salc=True
                    if conf.conta_fiscal and Usuario.objects.get(id_usuario=conf.conta_fiscal).nm_usuario==contadesteuser[1]:
                        is_fiscal=True
                    if conf.conta_od and Usuario.objects.get(id_usuario=conf.conta_od).nm_usuario==contadesteuser[1]:
                        is_od=True
                    if conf.conta_odsubstituto and Usuario.objects.get(id_usuario=conf.conta_odsubstituto).nm_usuario==contadesteuser[1]:
                        is_odsubstituto=True
            if "_requisitante" in vars['campo']: autorizado = True
            elif "_fiscal" in vars['campo'] and is_fiscal: autorizado = True
            elif "_od" in vars['campo'] and is_od: autorizado = True
            elif "_od" in vars['campo'] and is_odsubstituto:
                autorizado = True
                odsubstituto = "Substituto"
                dic['substituto']=vars['campo'].replace("ass_od","odsubstituto")
            else: 
                return HttpResponse('Unauthorized', status=401)
            dic['is_salc']=is_salc
            dic['is_fiscal']=is_fiscal
            dic['is_od']=is_od
            dic['is_odsubstituto']=is_odsubstituto
            # Pegar o conjunto de dados deste documento
            try:
                pr = Processo_requisitorio.objects.get(secao_ano_nr__exact=vars['processo'])
                #dbpg(dbpg.processo_requisitorio.secao_ano_nr==vars['processo']).select().first()
                dados = json.loads(pr.dados)
            except:
                # Não encontrou?
                return HttpResponse('Bad Request', status=400)
            # gerar uma código de assinatura
            lettersAndDigits = string.ascii_uppercase + string.digits
            flag = 1
            while flag>0 and flag<=10:
                try:
                    codigo = ''.join(random.choice(lettersAndDigits) for i in range(6))
                    a = Assinatura(cod=codigo,militar=militar,pr=vars['processo'],documento_assinado=vars['campo'])
                    a.save()
                    flag=0
                except Exception as e:
                    # chegar aqui significa "unique key constrait violation" no campo código
                    # Deve-se repetir essa iteração
                    flag = 1
            if flag>0:
                return HttpResponse('Internal Server Error', status=500)
            dic['codigo']=codigo
            assinatura = militar + " - " + codigo + " - " + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            # Atualizar o conjunto de dados deste documento
            dados[vars['campo']]=assinatura
            dados[vars['campo']+'_edited']='true'
            if "_od" in vars['campo']: dados[vars['campo'].replace("ass_od","odsubstituto")]=odsubstituto
            pr.dados=json.dumps(dados, sort_keys=True)
            pr.save()
            dic['assinatura'] = assinatura
            dic['hashed'] = CRYPT(pr.dados)
        if dic['comentar']:
            try:
                pessoa = Pessoa.objects.get(nm_login=request.user.username)
                autor = posto_graduacao(pessoa.cd_patente, 1) + " " + pessoa.nm_guerra+ " - "+ pessoa.nm_completo
                dic['autor']=autor
                dic['datahora']=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                dic['comentario']=vars.pop('comentario')
                c = Comentario(pr=vars.pop('processo'),
                            autor=autor,
                            comentario=dic['comentario'])
                c.save()
            except Exception as e:
                return HttpResponse(mark_safe(f'<h2>{e=}</h2>'), status=400)
        if dic['remline']:
            """
            """
            if vars['processo'].split("_")[0] not in secoes_deste_user:
                return HttpResponse(mark_safe('<h2>Usuário não pertence a esta seção.</h2>'), status=403)
            try:
                ordem=int(vars.pop('ord'))
                pr = Processo_requisitorio.objects.get(secao_ano_nr__exact=vars['processo'])
                dados = json.loads(pr.dados)
            except:
                # Não encontrou?
                return HttpResponse('Bad Request', status=400)
            if pr.valido!=None: 
                return HttpResponse(mark_safe('<h2>Este processo já foi encerrado.</h2>'), status=400)
            dic['vars']=[]
            countlinhas_pedido=[]
            variaveis_tipo_lista = ['nritem','descricaoitem','unidade','qtitens','valor','somaparcial','valorvencedor','valorcomparacao1',
                                    'valorcomparacao2','valorcomparacao3','unit2','unit3']
            variaveis_parecidas_com_lista = ['ncvalor']
            dados_copy = dados.copy()
            for k, v in dados_copy.items():
                if "-"+str(ordem) in k:
                    dic['vars'].append({k:dados.pop(k)})
                for val in variaveis_tipo_lista:
                    if val in k and "_edited" not in k and k not in variaveis_parecidas_com_lista:
                        # BUG: tinha um erro de listindex out of range aqui
                        # CORRIGIDO: adição de variaveis_parecidas_com_lista
                        try:
                            countlinhas_pedido.append(int(k.split("-")[1]))
                        except:
                            return HttpResponse(mark_safe(f'<h2>{k=}</h2>'), status=500)
                        break
            if countlinhas_pedido:
                countlinhas_pedido = max(countlinhas_pedido)
            else:
                countlinhas_pedido = 1
            dic['qtlinhas']=countlinhas_pedido
            while countlinhas_pedido>=ordem:
                ordem+=1
                dados_copy = dados.copy()
                for k, v in dados_copy.items():
                    if "-"+str(ordem) in k:
                        dados[k.replace("-"+str(ordem),"-"+str(ordem-1))]=dados.pop(k)
                        countlinhas_pedido+=1
            pr.dados = json.dumps(dados)
            pr.save()
        if dic["up"]:
            if vars['processo'].split("_")[0] not in secoes_deste_user:
                return JsonResponse({"error":"Usuário não pertence a esta seção."})
            if vars["modo"] == "carona": modo = "carona"
            elif vars["modo"] == "dispensa": modo = "dispensa"
            elif vars["modo"] == "inex": modo = "inex"
            else: return JsonResponse({"error":"Modo não permitido."})
            try:
                anexos_deste_processo = Anexo.objects.filter(pr__exact=vars['processo'])
                total = 0
                for a in anexos_deste_processo:
                    try:
                        total+=int(a.tamanho)
                    except:
                        pass
                filesize = len(request.FILES['file-data'])
                total+=filesize
                if total>settings.MAXSIZE*1024: 
                    return JsonResponse({"error":"Tamanho total dos arquivos (%s KB) maior que o limite máximo (%s KB)."%(str(total/1024),str(settings.MAXSIZE))})
                pr = Processo_requisitorio.objects.get(secao_ano_nr__exact=vars['processo'])
                if pr.valido!=None: 
                    return JsonResponse({"error":"Este processo já foi encerrado."})
                dados = json.loads(pr.dados)
                dados['modo']=modo
                filename = request.FILES['file-data'].name
                if filename.split(".")[-1] in allowed:
                    nid = Anexo(arquivo=request.FILES['file-data'],
                                modo=modo,
                                tamanho=str(filesize),
                                name=filename,
                                pr=vars['processo'])
                    nid.save()
                    pr.dados=json.dumps(dados)
                    pr.save()
                    return JsonResponse({
                            'initialPreviewAsData' : True,
                            'initialPreview' : 'download2/'+nid.name,
                            "initialPreviewConfig": [
                                {
                                    'key' : nid.id,
                                    'caption' : nid.name,
                                    'size' : nid.tamanho,
                                    'downloadUrl' : nid.arquivo.url,
                                    'url' : reverse('requisicoes:api')+'?del=1&processo='+vars['processo']
                                }
                            ]
                        })
                else:
                    return JsonResponse({"error":"Extensão não permitida"})
            except Exception as e:
                return HttpResponse(mark_safe(f'<h2>{e=}</h2>'), status=500)
        if dic["del"]:
            try:
                if vars['processo'].split("_")[0] not in secoes_deste_user:
                    return JsonResponse({"error":"Usuário não pertence a esta seção."})
                pr = Processo_requisitorio.objects.get(secao_ano_nr__exact=vars['processo'])
                if pr.valido!=None:
                    return JsonResponse({"error":"Este processo já foi encerrado."})
                try:
                    anexo_row = Anexo.objects.get(id=int(vars['key']))
                except:
                    return JsonResponse({"error":"Arquivo não encontrado!"})
                pr2 = anexo_row.pr
                if pr2.split("_")[0] not in secoes_deste_user:
                    return JsonResponse({"error":"Usuário não pertence a esta seção!"})
                if pr2!=vars['processo']:
                    return JsonResponse({"error":"Arquivo não pertence a este processo!"})
                anexo_row.delete()
            except Exception as e:
                return HttpResponse(mark_safe(f'<h2>{e=}</h2>'), status=500)
    elif request.method =='PUT':
        dic=dict(validar=False,invalidar=False,clonar=False)
        vars = request.GET.copy()
        vars.update(json.loads(request.body))
        dic['vars'] = vars.copy()
        for key, value in dic.items():
            if key in vars: dic.update({key:True if (vars[key] == "1" or vars[key] == "true") else False})
        if dic['validar']:
            # Pegar o conjunto de dados deste documento
            try:
                pr = Processo_requisitorio.objects.get(secao_ano_nr__exact=vars['processo'])
            except:
                # Não encontrou?
                return HttpResponse('Bad Request', status=400)
            if pr.valido!=None:
                return HttpResponse('Este processo já foi encerrado', status=400)
            pr.valido=True
            params = dict(secao=vars['processo'].split("_")[0],ano=vars['processo'].split("_")[-2],nr=vars['processo'].split("_")[-1])
            dic['redirect2']='?'+ urllib.parse.urlencode(params)
            pr.save()
        if dic['invalidar']:
            # Pegar o conjunto de dados deste documento
            try:
                pr = Processo_requisitorio.objects.get(secao_ano_nr__exact=vars['processo'])
            except:
                # Não encontrou?
                return HttpResponse('Bad Request', status=400)
            if pr.valido!=None: 
                return HttpResponse('Este processo já foi encerrado', status=400)
            pr.valido=False
            params = dict(secao=vars['processo'].split("_")[0],ano=vars['processo'].split("_")[-2],nr=vars['processo'].split("_")[-1])
            dic['redirect2']='?'+ urllib.parse.urlencode(params)
            pr.save()
        if dic['clonar']: # TODO: testar
            # Pegar o conjunto de dados deste documento
            try:
                pr = Processo_requisitorio.objects.get(secao_ano_nr__exact=vars['processo'])
                dados = json.loads(pr.dados)
                secao=vars['secao']
                ano=vars['ano'] if 'ano' in vars else datetime.now().strftime('%Y') # Brecha proposital
                resumo=vars['resumo']
                groups = secoes_deste_user
            except: # Não encontrou?
                return HttpResponse('Bad Request', status=400)
            # Checar novamente se ele tem permissão para inserir nesta seção
            if secao not in groups:
                return HttpResponse('Unauthorized', status=403)
            # montagem dos dados a serem inseridos
            try:
                last = Processo_requisitorio.objects.filter(secao_ano_nr__contains=secao+"_"+ano).order_by('id').last()
                # TODO: checar oq acpntece qd a seção n tem processos. last=None ou dá erro?
                nr = "%02d"%(int(last.secao_ano_nr.split("_")[-1])+1) if last else "01"
                dados["data"]=datetime.now().strftime('%d/%m/%Y')
                #1) Acabar com todas as assinaturas
                campos_assinados = [ k for k,v in dados.items() if "ass_" in k]
                for c in campos_assinados:
                    dados.pop(c)
            except Exception as e:
                return HttpResponse('Internal Server Error', status=500)
            # Inserção
            pr = Processo_requisitorio(secao_ano_nr=secao+'_'+ano+'_'+nr,
                                  resumo=resumo,
                                  dados=json.dumps(dados))
            dic['nr']=nr
            params = dict(secao=secao,ano=ano,nr=nr)
            dic['redirect2']='?'+ urllib.parse.urlencode(params)
            pr.save()
        dic['vars'] = vars.copy()
    elif request.method =='DELETE':
        dic = dict()
    return JsonResponse(dic)