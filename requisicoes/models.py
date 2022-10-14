from django.db import models
from django.utils.html import mark_safe
from django.core.validators import int_list_validator

"""
class Configuracao(models.Model):
    contas_salc = models.ManyToManyField(Usuario, blank=True, help_text=mark_safe("Contas do SPED autorizadas a executar as ações da <b>SALC</b>:"))
    conta_fiscal = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='fiscal', blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Fiscal Administrativo</b>:"))
    conta_od = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='od',blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Ordenador de Despesas</b>:"))
    conta_odsubstituto = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='odsubstituto',blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar como <b>Ordenador de Despesas Substituto</b>:"))
    class Meta:
        verbose_name_plural = "Configurações"
        db_table = 'configuracao'
"""
class Configuracao(models.Model):
    contas_salc = models.CharField(validators=[int_list_validator],blank=True,null=True, max_length=100, help_text=mark_safe("Contas do SPED autorizadas a executar as ações da <b>SALC</b>:"))
    conta_fiscal = models.IntegerField(blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Fiscal Administrativo</b>:"))
    conta_od = models.IntegerField(blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Ordenador de Despesas</b>:"))
    conta_odsubstituto = models.IntegerField(blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar como <b>Ordenador de Despesas Substituto</b>:"))
    class Meta:
        verbose_name_plural = "Configurações"
        db_table = 'configuracao'
"""

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