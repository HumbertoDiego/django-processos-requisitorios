from django.contrib import admin
from .models import Configuracao

class MyConfiguracaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Configuracao,MyConfiguracaoAdmin)