from django.contrib import admin

from .models import Usuario, Usuario_Pessoa, Usuario_Secao, Pessoa, Secao

class MyUsuarioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Usuario,MyUsuarioAdmin)

class MyPessoaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Pessoa,MyPessoaAdmin)

class MySecaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Secao,MySecaoAdmin)

class MyUsuario_PessoaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Usuario_Pessoa,MyUsuario_PessoaAdmin)

class MyUsuario_SecaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Usuario_Secao,MyUsuario_SecaoAdmin)
