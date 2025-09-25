from django import forms
from .models import Conta

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }