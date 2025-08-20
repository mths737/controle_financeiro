from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ClienteViewSet, CategoriaViewSet, ContaViewSet
from .views import home, cliente_list, categoria_list, conta_list, dashboard, marcar_como_pago

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'contas', ContaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('clientes/', cliente_list, name='cliente_list'),

    path('categorias/', categoria_list, name='categoria_list'),

    path('contas/', conta_list, name='conta_list'),
    path('conta/<int:pk>/pagar/', marcar_como_pago, name='marcar_como_pago'),

    path('dashboard/', dashboard, name='dashboard'),
    path('', home),
]