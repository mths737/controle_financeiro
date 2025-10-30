from django.urls import path
from .views import categoria_list

app_name = 'categorias'

urlpatterns = [
    path('', categoria_list, name='categoria_list'),
]