from rest_framework import viewsets
from .models import Conta
from .serializers import ContaSerializer
from rest_framework.permissions import IsAuthenticated

class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAuthenticated]