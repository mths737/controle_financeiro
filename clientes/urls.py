from django.urls import path
from .views import cliente_list


app_name = 'clientes'

urlpatterns = [
    path('', cliente_list, name='cliente_list'),
]