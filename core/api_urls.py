from rest_framework.routers import DefaultRouter
from contas.api_views import ContaViewSet
from clientes.api_views import ClienteViewSet
from categorias.api_views import CategoriaViewSet

router = DefaultRouter()
router.register(r'contas', ContaViewSet, basename='contas')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'categorias', CategoriaViewSet, basename='categorias')

urlpatterns = router.urls