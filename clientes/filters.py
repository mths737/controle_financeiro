import django_filters
from django.db.models import Q
from .models import Cliente

class ClienteFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Buscar")

    class Meta:
        model = Cliente
        fields = []  # só usamos o search customizado

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nome__icontains=value) |
            Q(cpf_cnpj__icontains=value) |
            Q(telefone__icontains=value) |
            Q(email__icontains=value)
        )