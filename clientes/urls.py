from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ClienteViewSet
from .views import cliente_list

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)

app_name = 'clientes'

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('', cliente_list, name='cliente_list'),

]