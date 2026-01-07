from django.db import models

def upload_logo(instance, filename):
    ext = filename.split('.')[-1]  # pega extensão
    return f"logos/logo.{ext}"

class Configuracao(models.Model):
    nome_empresa = models.CharField(max_length=100, default="Minha Empresa")
    logo = models.ImageField(upload_to=upload_logo, blank=True, null=True)
    tema = models.CharField(max_length=20, choices=[
        ('light', 'Claro'),
        ('dark', 'Escuro'),
    ], default='light')
    email_suporte = models.EmailField(blank=True, null=True)
    telefone_suporte = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "Configurações do Sistema"