import django_filters
from django.db.models import Q
from .models import Conta

class ContaFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Buscar")
    data_inicio = django_filters.DateFilter(field_name="data_vencimento", lookup_expr='gte', label="Data inicial")
    data_fim = django_filters.DateFilter(field_name="data_vencimento", lookup_expr='lte', label="Data final")
    valor_min = django_filters.NumberFilter(field_name="valor", lookup_expr='gte', label="Valor mínimo")
    valor_max = django_filters.NumberFilter(field_name="valor", lookup_expr='lte', label="Valor máximo")

    class Meta:
        model = Conta
        fields = []  # não usamos os padrões, só os customizados

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(cliente__nome__icontains=value) |
            Q(cliente__cpf_cnpj__icontains=value) |
            Q(cliente__telefone__icontains=value) |
            Q(cliente__email__icontains=value) |
            Q(categoria__nome__icontains=value) |
            Q(data_vencimento__icontains=value) |
            Q(data_pagamento__icontains=value) |
            Q(valor__icontains=value) |
            Q(tipo__icontains=value)
        )