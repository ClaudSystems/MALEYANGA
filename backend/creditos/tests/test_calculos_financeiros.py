# credito/tests/test_calculos_financeiros.py
from decimal import Decimal
from django.test import TestCase
from ..utils.calculos_financeiros import CalculosFinanceiros

class TestCalculosFinanceiros(TestCase):
    
    def test_pmt_taxa_zero(self):
        """Teste PMT com taxa zero"""
        resultado = CalculosFinanceiros.pmt(Decimal('0.00'), 12, Decimal('1200.00'))
        self.assertEqual(resultado, Decimal('100.00'))
    
    def test_pmt_taxa_positiva(self):
        """Teste PMT com taxa positiva"""
        resultado = CalculosFinanceiros.pmt(Decimal('0.01'), 12, Decimal('1000.00'))
        # Valor esperado calculado externamente
        self.assertEqual(resultado, Decimal('88.85'))
    
    def test_tabela_price_consistente(self):
        """Teste se a tabela Price é matematicamente consistente"""
        tabela = CalculosFinanceiros.gerar_tabela_price(
            Decimal('1000.00'), Decimal('12.00'), 12, "mensal"
        )
        
        # Verificar se a soma das amortizações iguala o valor do empréstimo
        total_amortizacao = sum(item['amortizacao'] for item in tabela)
        self.assertEqual(total_amortizacao, Decimal('1000.00'))
        
        # Verificar se o saldo final é zero
        self.assertEqual(tabela[-1]['saldo_devedor'], Decimal('0.00'))