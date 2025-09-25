from datetime import date
from django.db import models
from clientes.models import Cliente
from categorias.models import Categoria

class Conta(models.Model):
    TIPO_CHOICES = (
        ('P', 'Pagar'),
        ('R', 'Receber'),
    )

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)

    @property
    def status(self):
        today = date.today()
        if self.data_pagamento:
            return "Pago"
        elif self.data_vencimento < today:
            return "Atrasado"
        else:
            return "Pendente"

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.cliente.nome}'