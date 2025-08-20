from django.contrib import admin

from .models import Cliente, Categoria, Conta
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Conta)