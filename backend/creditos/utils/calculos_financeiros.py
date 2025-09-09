# credito/utils/calculos_financeiros.py
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext
import math
from typing import Literal

class CalculosFinanceiros:
    """
    Classe para cálculos financeiros corretos e consistentes
    Implementa métodos testados e validados matematicamente
    """
    
    # Mapas de periodicidade (mantidos para referência)
    PERIODICIDADE_DIAS = {
        "mensal": 30,
        "quinzenal": 15,
        "semanal": 7,
        "diario": 1,
        "doisdias": 2,
        "variavel": 30  # default
    }
    
    PERIODOS_POR_ANO = {
        "mensal": 12,
        "quinzenal": 24,
        "semanal": 52,
        "diario": 365,
        "doisdias": 182,
        "variavel": 12  # default
    }

    @staticmethod
    def pmt(
        taxa_periodica: Decimal,
        numero_periodos: int,
        valor_presente: Decimal,
        valor_futuro: Decimal = Decimal('0.00'),
        tipo: Literal[0, 1] = 0
    ) -> Decimal:
        """
        Calcula o pagamento periódico (PMT) usando a fórmula correta
        tipo 0: pagamentos no final do período
        tipo 1: pagamentos no início do período
        """
        if numero_periodos <= 0:
            raise ValueError("Número de períodos deve ser maior que zero")
        
        if taxa_periodica < Decimal('0.00'):
            raise ValueError("Taxa não pode ser negativa")
        
        # Para taxa zero, pagamento é simplesmente VP/nper
        if taxa_periodica == Decimal('0.00'):
            return (valor_presente - valor_futuro) / Decimal(numero_periodos)
        
        taxa = taxa_periodica
        fator = (Decimal('1.00') + taxa) ** numero_periodos
        
        if tipo == 0:  # Pagamentos no final do período
            pmt = (valor_presente * taxa * fator) / (fator - Decimal('1.00'))
            if valor_futuro != Decimal('0.00'):
                pmt -= valor_futuro * taxa / (fator - Decimal('1.00'))
        else:  # Pagamentos no início do período
            pmt = (valor_presente * taxa * fator) / ((fator - Decimal('1.00')) * (Decimal('1.00') + taxa))
            if valor_futuro != Decimal('0.00'):
                pmt -= valor_futuro * taxa / ((fator - Decimal('1.00')) * (Decimal('1.00') + taxa))
        
        return pmt.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @staticmethod
    def calcular_taxa_periodica(
        taxa_anual: Decimal, 
        periodicidade: str, 
        dias_periodo: int = None
    ) -> Decimal:
        """
        Converte taxa anual para taxa periódica de forma correta
        """
        taxa_anual_decimal = taxa_anual / Decimal('100.00')
        
        if periodicidade == "variavel" and dias_periodo:
            # Para periodicidade variável, usar dias específicos
            periodos_ano = Decimal('365.00') / Decimal(str(dias_periodo))
        else:
            periodos_ano = Decimal(str(CalculosFinanceiros.PERIODOS_POR_ANO.get(periodicidade, 12)))
        
        # Taxa periódica = (1 + taxa_anual)^(1/periodos_ano) - 1
        taxa_periodica = (Decimal('1.00') + taxa_anual_decimal) ** (Decimal('1.00') / periodos_ano) - Decimal('1.00')
        
        return taxa_periodica.quantize(Decimal('0.00000001'), rounding=ROUND_HALF_UP)

    @staticmethod
    def gerar_tabela_price(
        valor_emprestimo: Decimal,
        taxa_anual: Decimal,
        numero_prestacoes: int,
        periodicidade: str = "mensal",
        dias_periodo: int = None
    ) -> list:
        """
        Gera tabela Price completa com amortização, juros e saldo devedor
        """
        taxa_periodica = CalculosFinanceiros.calcular_taxa_periodica(taxa_anual, periodicidade, dias_periodo)
        prestacao = CalculosFinanceiros.pmt(taxa_periodica, numero_prestacoes, valor_emprestimo)
        
        tabela = []
        saldo_devedor = valor_emprestimo
        
        for periodo in range(1, numero_prestacoes + 1):
            juros_periodo = saldo_devedor * taxa_periodica
            amortizacao = prestacao - juros_periodo
            saldo_devedor -= amortizacao
            
            # Ajuste para última prestação (evitar centavos perdidos)
            if periodo == numero_prestacoes:
                amortizacao += saldo_devedor
                saldo_devedor = Decimal('0.00')
            
            tabela.append({
                'periodo': periodo,
                'prestacao': prestacao.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'juros': juros_periodo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'amortizacao': amortizacao.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'saldo_devedor': saldo_devedor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            })
        
        return tabela

    @staticmethod
    def calcular_sistema_amortizacao_constante(
        valor_emprestimo: Decimal,
        taxa_anual: Decimal,
        numero_prestacoes: int,
        periodicidade: str = "mensal",
        dias_periodo: int = None
    ) -> list:
        """
        Sistema de amortização constante (SAC)
        """
        taxa_periodica = CalculosFinanceiros.calcular_taxa_periodica(taxa_anual, periodicidade, dias_periodo)
        amortizacao_constante = valor_emprestimo / Decimal(numero_prestacoes)
        
        tabela = []
        saldo_devedor = valor_emprestimo
        
        for periodo in range(1, numero_prestacoes + 1):
            juros_periodo = saldo_devedor * taxa_periodica
            prestacao = amortizacao_constante + juros_periodo
            saldo_devedor -= amortizacao_constante
            
            tabela.append({
                'periodo': periodo,
                'prestacao': prestacao.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'juros': juros_periodo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'amortizacao': amortizacao_constante.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'saldo_devedor': saldo_devedor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            })
        
        return tabela

    @staticmethod
    def calcular_juros_mora_corretos(
        valor_devido: Decimal,
        percentual_juros_mora: Decimal,
        dias_mora: int,
        capitalizacao_diaria: bool = False
    ) -> Decimal:
        """
        Calcula juros de mora de forma correta, com opção de capitalização diária
        """
        if dias_mora <= 0 or valor_devido >= Decimal('0.00'):
            return Decimal('0.00')
        
        taxa_diaria = percentual_juros_mora / Decimal('100.00') / Decimal('365.00')
        
        if capitalizacao_diaria:
            # Juros compostos diários
            juros_mora = valor_devido * ((Decimal('1.00') + taxa_diaria) ** dias_mora - Decimal('1.00'))
        else:
            # Juros simples
            juros_mora = valor_devido * taxa_diaria * Decimal(dias_mora)
        
        return abs(juros_mora).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)