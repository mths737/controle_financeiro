from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
