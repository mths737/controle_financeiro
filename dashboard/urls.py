from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard, dashboard_view

router = DefaultRouter()

app_name = 'dashboard'

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += [
    path('', dashboard, name='dashboard'),
    path('2', dashboard_view, name='dashboard2'),
]