from rest_framework import viewsets
# Mude a permissão de AllowAny para IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from .models import Cliente, Assinante
from .serializers import ClienteSerializer, AssinanteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que clientes sejam visualizados ou editados.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    # Agora a API só aceita requisições com um token JWT válido
    permission_classes = [IsAuthenticated]


class AssinanteViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que assinantes sejam visualizados ou editados.
    """
    queryset = Assinante.objects.all()
    serializer_class = AssinanteSerializer
    # Agora a API só aceita requisições com um token JWT válido
    permission_classes = [IsAuthenticated]
