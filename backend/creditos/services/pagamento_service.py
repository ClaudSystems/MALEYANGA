# credito/services/pagamento_service.py
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from ..models import Pagamento
from ..utils.calculos_financeiros import CalculosFinanceiros

class PagamentoService:
    
    @transaction.atomic
    def criar_pagamentos_credito(self, credito):
        """Cria pagamentos para um crédito"""
        if credito.forma_de_calculo == 'pmt':
            tabela = CalculosFinanceiros.gerar_tabela_price(
                credito.valor_creditado,
                credito.percentual_de_juros,
                credito.numero_de_prestacoes,
                credito.periodicidade,
                credito.periodo_variavel
            )
        else:
            tabela = CalculosFinanceiros.calcular_sistema_amortizacao_constante(
                credito.valor_creditado,
                credito.percentual_de_juros,
                credito.numero_de_prestacoes,
                credito.periodicidade,
                credito.periodo_variavel
            )
        
        pagamentos = []
        data_base = credito.date_concecao
        
        for i, prestacao in enumerate(tabela, 1):
            data_pagamento = self._calcular_data_pagamento(data_base, credito.periodicidade, credito.periodo_variavel)
            
            pagamento = Pagamento(
                credito=credito,
                descricao=f"{i}ª Prestação",
                numero_de_pagamento=f"{credito.numero_do_credito}-{i:03d}",
                valor_da_prestacao=prestacao['prestacao'],
                valor_de_juros=prestacao['juros'],
                valor_de_amortizacao=prestacao['amortizacao'],
                saldo_devedor=prestacao['saldo_devedor'],
                data_previsto_de_pagamento=data_pagamento,
                recorencia_de_moras=credito.recorencia_de_moras or 1
            )
            
            pagamentos.append(pagamento)
            data_base = data_pagamento
        
        Pagamento.objects.bulk_create(pagamentos)
        return pagamentos

    def _calcular_data_pagamento(self, data_base, periodicidade, periodo_variavel=None):
        """Calcula data de pagamento de forma simplificada"""
        from datetime import timedelta
        
        dias_por_periodicidade = {
            'mensal': 30, 'quinzenal': 15, 'semanal': 7,
            'diario': 1, 'doisdias': 2, 'variavel': periodo_variavel or 30
        }
        
        dias = dias_por_periodicidade.get(periodicidade, 30)
        return data_base + timedelta(days=dias)