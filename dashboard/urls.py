from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard_view

router = DefaultRouter()

app_name = 'dashboard'

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('', dashboard_view, name='dashboard'),
]