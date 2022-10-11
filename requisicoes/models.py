from django.db import models
import os
from django.conf import settings
from django.core.validators import int_list_validator
from django.utils.html import mark_safe
from django.dispatch import receiver

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nm_usuario = models.CharField(max_length=50)
    in_excluido = models.CharField(max_length=2)
    def __str__(self):
        return '{} - {}'.format(self.id_usuario, self.nm_usuario)
    class Meta:
        verbose_name_plural = "Usuários"

class Pessoa(models.Model):
    id_pessoa = models.AutoField(primary_key=True)
    nm_login = models.CharField(max_length=50)
    nm_completo = models.CharField(max_length=150)
    cd_patente = models.IntegerField()
    nm_guerra = models.CharField(max_length=50)
    def __str__(self):
        return '{} - {} - {}'.format(self.id_pessoa, self.nm_guerra, self.nm_completo)

class Secao(models.Model):
    id_secao = models.AutoField(primary_key=True)
    id_pai = models.IntegerField()
    nm_sigla = models.CharField(max_length=50)
    in_excluido = models.CharField(max_length=2)
    def __str__(self):
        return '{} - {}'.format(self.id_secao, self.nm_sigla)

class Usuario_Pessoa(models.Model):
    id_usuario_pessoa = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    dt_fim = models.CharField(max_length=50)

class Usuario_Secao(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_secao = models.ForeignKey(Secao, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('id_usuario', 'id_secao'),)


class Configuracao(models.Model):
    contas_salc = models.ManyToManyField(Usuario, blank=True, help_text=mark_safe("Contas do SPED autorizadas a executar as ações da <b>SALC</b>:"))
    conta_fiscal = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='fiscal', blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Fiscal Administrativo</b>:"))
    conta_od = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='od',blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Ordenador de Despesas</b>:"))
    conta_odsubstituto = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name='odsubstituto',blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar como <b>Ordenador de Despesas Substituto</b>:"))
    class Meta:
        verbose_name_plural = "Configurações"
"""
dbpgsped.define_table('usuario_secao',
                    Field('id_usuario',dbpgsped.usuario),
                    Field('id_secao',dbpgsped.secao),
                    primarykey=['id_usuario', 'id_secao'],
                    migrate=migrate_bool
                    )
dbpg = DAL(DBPG_URI,
            pool_size=configuration.get('dbpg.pool_size'),
            migrate_enabled=configuration.get('dbpg.migrate'),
            check_reserved=['all'])

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