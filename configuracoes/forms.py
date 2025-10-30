from django import forms
from .models import Configuracao

class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        fields = '__all__'