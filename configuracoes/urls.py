from django.urls import path
from . import views

app_name = 'configuracoes'

urlpatterns = [
    path('', views.configuracao_view, name='configuracao'),
]