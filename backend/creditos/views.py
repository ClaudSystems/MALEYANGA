# creditos/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Credito, Pagamento, Parcela, Remissao
from .serializers import (
    CreditoSerializer, 
    PagamentoSerializer, 
    ParcelaSerializer, 
    RemissaoSerializer
)

class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtra créditos por usuário ou todos se for superuser
        if self.request.user.is_superuser:
            return Credito.objects.all()
        return Credito.objects.filter(utilizador=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(utilizador=self.request.user)
    
    @action(detail=True, methods=['post'])
    def atualizar_estado(self, request, pk=None):
        credito = self.get_object()
        credito.atualizar_estado()
        credito.save()
        return Response({'status': 'Estado atualizado'})
    
    @action(detail=True, methods=['get'])
    def calcular_totais(self, request, pk=None):
        credito = self.get_object()
        total_pago = credito.calcular_total_pago()
        total_moras = credito.calcular_total_moras()
        valor_em_divida = credito.calcular_valor_em_divida()
        
        return Response({
            'total_pago': total_pago,
            'total_moras': total_moras,
            'valor_em_divida': valor_em_divida
        })

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtra pagamentos por crédito do usuário
        if self.request.user.is_superuser:
            return Pagamento.objects.all()
        return Pagamento.objects.filter(credito__utilizador=self.request.user)

class ParcelaViewSet(viewsets.ModelViewSet):
    queryset = Parcela.objects.all()
    serializer_class = ParcelaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Parcela.objects.all()
        return Parcela.objects.filter(pagamento__credito__utilizador=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(utilizador=self.request.user)

class RemissaoViewSet(viewsets.ModelViewSet):
    queryset = Remissao.objects.all()
    serializer_class = RemissaoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Remissao.objects.all()
        return Remissao.objects.filter(pagamento__credito__utilizador=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(utilizador=self.request.user)