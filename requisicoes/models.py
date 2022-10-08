from django.db import models

# Create your models here.

"""
dbpg = DAL(DBPG_URI,
            pool_size=configuration.get('dbpg.pool_size'),
            migrate_enabled=configuration.get('dbpg.migrate'),
            check_reserved=['all'])

dbpg.define_table('configuracoes',
    Field("contas_salc", type='list:integer', label=XML("Contas do SPED autorizadas a executar as ações da <b>SALC</b>:")),
    Field("conta_fiscal", type='integer', label=XML("Conta do SPED autorizada a assinar em <b>Fiscal Administrativo</b>:")),
    Field("conta_od", type='integer', label=XML("Conta do SPED autorizada a assinar em <b>Ordenador de Despesas</b>:")),
    Field("conta_odsubstituto", type='integer', label=XML("Conta do SPED autorizada a assinar como <b>Ordenador de Despesas Substituto</b>:")),
    migrate=migrate_bool
)

dbpg.define_table('processo_requisitorio',
    Field('secao_ano_nr', required=True, unique=True),
    Field('resumo', required=True),
    Field('valido', 'boolean'),
    Field('dados', 'text'),
    migrate=migrate_bool)

dbpg.define_table('assinaturas',
    Field('cod', unique=True),
    Field('militar'),
    Field('datahora', type="datetime", label='Hora da Assinatura',default=request.now,requires = IS_DATETIME(format=('%d-%m-%Y %H:%M:%S'))),
    Field('pr'),
    Field('documento_assinado'),
    migrate=migrate_bool)

dbpg.define_table('anexos',
    Field('pr', required=True),
    Field('modo', required=True),
    Field('tamanho'),
    Field('name'),
    Field('arquivo', 'upload', autodelete=True, required=True, requires=IS_LENGTH(MAXSIZE*1024, 1, error_message='Max image size: %s KB'%str(MAXSIZE))),
                  # requires=IS_IMAGE(extensions=('jpeg', 'png','jpg','tif'))),
    migrate=migrate_bool)

dbpg.define_table('comentarios',
    Field('pr', required=True),
    Field('autor', required=True),
    Field('comentario', required=True),
    Field('datahora', type="datetime",default=request.now, requires = IS_DATETIME(format=('%d-%m-%Y %H:%M:%S'))),
    migrate=migrate_bool)
"""