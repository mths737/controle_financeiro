from rest_framework import viewsets
from .models import Conta
from .serializers import ContaSerializer

class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer