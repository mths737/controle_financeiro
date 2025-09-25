from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CategoriaViewSet
from .views import categoria_list

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)

app_name = 'categorias'

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('', categoria_list, name='categoria_list'),

]