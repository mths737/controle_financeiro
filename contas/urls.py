from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ContaViewSet
from .views import conta_list, marcar_como_pago

router = DefaultRouter()
router.register(r'contas', ContaViewSet)

app_name = 'contas'

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('', conta_list, name='conta_list'),
    path('conta/<int:pk>/pagar/', marcar_como_pago, name='marcar_como_pago'),
]