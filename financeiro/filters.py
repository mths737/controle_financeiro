import django_filters
from .models import Conta

class ContaFilter(django_filters.FilterSet):
    cliente = django_filters.CharFilter(field_name='cliente__nome', lookup_expr='icontains', label="Cliente")
    categoria = django_filters.CharFilter(field_name='categoria__nome', lookup_expr='icontains', label="Categoria")

    class Meta:
        model = Conta
        fields = ['cliente', 'categoria']