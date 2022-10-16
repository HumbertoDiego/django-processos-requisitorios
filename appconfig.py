# App configuration,
# conta_admin --> Conta do SPED com permissões de configurar o app em https://[IP]/requisicoes/default/conf,
app = {
"name"         : "Processos Requisitórios",
"author"       : "Humberto Diego Aguiar Alves <diego.alves@eb.mil.br>",
"description"  : "App para confecção de processos requisitórios baseado nos usuários e seções do SPED",
"keywords"     : ["django", "python", "framework"],
"generator"    : "Django Web Framework",
"timbre_linha1": "MINISTÉRIO DA DEFESA",
"timbre_linha2": "EXÉRCITO BRASILEIRO",
"timbre_linha3": "DCT - DSG",
"timbre_linha4": "4º CENTRO DE GEOINFORMAÇÃO",
"orgabrev"     : "4º CGEO",
"orgendereco"  : "Avenida Marechal Bittencourt, nº 97, bairro Santo Antônio, CEP – 69029-160, em Manaus/AM",
"orgcidade"    : "Manaus",
"orgestado"    : "Amazonas",
"orgestadoabrev": "AM",
"orgextenso"   : "4º Centro de Geoinformação",
"ug"           : "160011",
"allowed_ext"  : ["txt","ini","md","json","geojson","png","jpg","jpeg","odt","ods","odp","doc","docx","xls","xlsx","ppt","pptx","pdf","zip","rar","tar","gzip","gz","7z"],
"conta_admin"  : ("Admin",1), # O id_usuario é o que de fato será utilizado para validação
"secao_escape" : "DGEO", # o escape é usado qd o usuario não define um secao
"maxtotalfsize": 8000, # maxfilesize em Kbytes
"url_creditos_disponveis": '#',
"url_modelo_solicitacao_aceite": '#',
"url_modelo_solicitacao_orcamento": '#',
"url_modelo_comprovante_exclusividade": '#'
}
# Host configuration,
host = {
    "names": ["localhost:*", "127.0.0.1:*", "*:*", "*"]
}
# db configuration,
db = {
    "uri"      : "sqlite://storage.sqlite",
    "migrate"  : True,
    "pool_size": 10
}
# sped configuration --> Preferencial --> Banco com a distribição dos usuários e LDAP para autenticação,
sped = {
    "host"     : '',
    "uri"      : '',
    "base_dn"  : 'dc=eb,dc=mil,dc=br',
    "pool_size": 10
}
# ldap configuration --> Banco com a distribição dos usuários e LDAP para autenticação caso sped.uri vazio,
ldap = {
    "host"     : 'ldap',
    "base_dn"  : 'dc=eb,dc=mil,dc=br',
    "pool_size": 10
}
# dbpg configuration
dbpg = {
    "host"     : 'post',
    "migrate"  : True,
    "pool_size": 10
}