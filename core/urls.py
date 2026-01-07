from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from core import settings

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)