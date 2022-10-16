from django.db import models
from django.utils.html import mark_safe
from django.core.validators import int_list_validator, FileExtensionValidator
import os
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.conf import settings
from appconfig import app

class Configuracao(models.Model):
    contas_salc = models.CharField(validators=[int_list_validator],blank=True,null=True, max_length=100, help_text=mark_safe("Contas do SPED autorizadas a executar as ações da <b>SALC</b>:"))
    conta_fiscal = models.IntegerField(blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Fiscal Administrativo</b>:"))
    conta_od = models.IntegerField(blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar em <b>Ordenador de Despesas</b>:"))
    conta_odsubstituto = models.IntegerField(blank=True,null=True, help_text=mark_safe("Conta do SPED autorizada a assinar como <b>Ordenador de Despesas Substituto</b>:"))
    class Meta:
        verbose_name_plural = "Configurações"
        db_table = 'configuracao'
    def __str__(self):
        return 'SALC:{} / Fiscal:{} / OD:{} / OD Substituto:{}'.format(self.contas_salc, self.conta_fiscal, self.conta_od, self.conta_odsubstituto or '')

class Processo_requisitorio(models.Model):
    secao_ano_nr = models.CharField(max_length=100 ,unique=True)
    resumo = models.CharField(max_length=200)
    valido = models.BooleanField(null=True)
    dados = models.TextField()
    class Meta:
        verbose_name_plural = "Processos"
        db_table = 'processo_requisitorio'

class Assinatura(models.Model):
    cod = models.CharField(max_length=10 ,unique=True)
    militar = models.CharField(max_length=100)
    datahora = models.DateTimeField(auto_now_add=True, help_text="Hora da Assinatura")
    pr = models.CharField(max_length=100)
    documento_assinado = models.CharField(max_length=100)
    class Meta:
        db_table = 'assinatura'

def update_filename(instance, filename):
    path = "anexos/"
    format = instance.userid + instance.transaction_uuid + instance.file_extension
    return os.path.join(path, format)

def file_size(value): # add this to some file where you can import it from
    limit = settings.MAXSIZE * 1024
    if value.size > limit:
        raise ValidationError('Max image size: %s KB'%(settings.MAXSIZE))

class Anexo(models.Model):
    pr = models.CharField(max_length=100 ,unique=True)
    modo = models.CharField(max_length=100)
    tamanho = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to=update_filename, validators=[file_size, FileExtensionValidator( settings.ALLOWED )])
    class Meta:
        db_table = 'anexo'

# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=Anexo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Anexo` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=Anexo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Anexo` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = Anexo.objects.get(pk=instance.pk).file
    except Anexo.DoesNotExist:
        return False
    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class Comentario(models.Model):
    pr = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    comentario = models.CharField(max_length=200)
    datahora = models.DateTimeField(auto_now_add=True, help_text="Hora da Assinatura")
    class Meta:
        db_table = 'comentario'