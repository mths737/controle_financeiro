from django import forms
from .models import Cliente, Categoria, Conta

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['ativo']
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }