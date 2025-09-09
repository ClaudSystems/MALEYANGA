# credito/services/credito_service.py
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ..models import Credito
from .pagamento_service import PagamentoService

class CreditoService:
    
    @transaction.atomic
    def criar_credito(self, dados_credito, user_id=None):
        """
        Cria um novo crédito de forma simplificada
        """
        try:
            if user_id:
                user = User.objects.get(id=user_id)
                dados_credito['utilizador'] = user
            
            credito = Credito(**dados_credito)
            credito.full_clean()
            credito.save()
            
            # Criar pagamentos automaticamente
            pagamento_service = PagamentoService()
            pagamento_service.criar_pagamentos_credito(credito)
            
            return credito
            
        except User.DoesNotExist:
            raise ValueError("Utilizador não encontrado")
        except ValidationError as e:
            raise e

    def listar_creditos(self, filtros=None):
        """Lista créditos com filtros opcionais"""
        queryset = Credito.objects.filter(invalido=False)
        
        if filtros:
            if 'cliente_id' in filtros:
                queryset = queryset.filter(cliente_id=filtros['cliente_id'])
            if 'estado' in filtros:
                queryset = queryset.filter(estado=filtros['estado'])
            if 'em_mora' in filtros:
                queryset = queryset.filter(em_mora=filtros['em_mora'])
        
        return queryset.order_by('-date_created')

    @transaction.atomic
    def atualizar_estado_credito(self, credito_id):
        """Atualiza o estado de um crédito"""
        try:
            credito = Credito.objects.get(id=credito_id)
            credito.atualizar_estado()
            credito.save()
            return credito
        except Credito.DoesNotExist:
            raise ValueError("Crédito não encontrado")