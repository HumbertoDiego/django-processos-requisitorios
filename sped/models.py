from django.db import models
from django.utils.html import mark_safe
import os

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nm_usuario = models.CharField(max_length=50)
    in_excluido = models.CharField(max_length=2)
    def __str__(self):
        return '({}) {}'.format(self.id_usuario, self.nm_usuario)
    class Meta:
        verbose_name_plural = "Usuários"
        db_table = 'usuario'
        #app_label = os.environ['POST_AUTHDB']

class Pessoa(models.Model):
    id_pessoa = models.AutoField(primary_key=True)
    nm_login = models.CharField(max_length=50)
    nm_completo = models.CharField(max_length=150)
    cd_patente = models.IntegerField()
    nm_guerra = models.CharField(max_length=50)
    def __str__(self):
        return '({}) {}'.format(self.id_pessoa, self.nm_guerra)
    class Meta:
        db_table = 'pessoa'

class Secao(models.Model):
    id_secao = models.AutoField(primary_key=True)
    id_pai = models.IntegerField(null=True)
    nm_sigla = models.CharField(max_length=50)
    in_excluido = models.CharField(max_length=2)
    def __str__(self):
        return '({}) {}'.format(self.id_secao, self.nm_sigla)
    class Meta:
        verbose_name_plural = "Seções"
        db_table = 'secao'

class Usuario_Pessoa(models.Model):
    id_usuario_pessoa = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,db_column='id_usuario')
    id_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE,db_column='id_pessoa')
    dt_fim = models.CharField(max_length=50,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Usuários (Contas) de Pessoas"
        db_table = 'usuario_pessoa'
    def __str__(self):
        return '{}_{} '.format(self.id_usuario, self.id_pessoa)


class Usuario_Secao(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,db_column='id_usuario')
    id_secao = models.ForeignKey(Secao, on_delete=models.CASCADE,db_column='id_secao')
    def __str__(self):
        return '{}_{}'.format(self.id_usuario, self.id_secao)
    class Meta:
        unique_together = (('id_usuario', 'id_secao'),)
        verbose_name_plural = "Usuários (Contas) de Seções"
        db_table = 'usuario_secao'