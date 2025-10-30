from django.contrib import admin

from .models import Cliente
admin.site.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf_cnpj", "telefone", "email")
    search_fields = ("nome", "cpf_cnpj")
    list_filter = ("ativo",)