from django.contrib import admin
from models import Usuario, Usuario_Pessoa, Usuario_Secao, Pessoa, Secao, Configuracao

class MyUsuarioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Usuario,MyUsuarioAdmin)