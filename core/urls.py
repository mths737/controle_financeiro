from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('contas/', include('contas.urls')),
    path('categorias/', include('categorias.urls')),
    path('clientes/', include('clientes.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('core.api_urls')),
    path('configuracoes/', include('configuracoes.urls')),
]