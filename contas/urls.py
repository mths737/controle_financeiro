from django.urls import path
from .views import conta_list, marcar_como_pago

app_name = 'contas'

urlpatterns = [
    path('', conta_list, name='conta_list'),
    path('conta/<int:pk>/pagar/', marcar_como_pago, name='marcar_como_pago'),
]