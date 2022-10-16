from django.contrib import admin
from .models import Configuracao, Processo_requisitorio, Assinatura, Anexo, Comentario

class MyConfiguracaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Configuracao,MyConfiguracaoAdmin)

class MyProcesso_requisitorioAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    pass
admin.site.register(Processo_requisitorio,MyProcesso_requisitorioAdmin)

class MyAssinaturaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    pass
admin.site.register(Assinatura,MyAssinaturaAdmin)

class MyAnexoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Anexo,MyAnexoAdmin)

class MyComentarioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comentario,MyComentarioAdmin)