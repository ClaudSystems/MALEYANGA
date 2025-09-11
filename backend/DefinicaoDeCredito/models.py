from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from taxas.models import Taxa  # Ajuste conforme sua estrutura


class DefinicaoDeCredito(models.Model):
    PERIODICIDADE_CHOICES = [
        ('diaria', 'Diária'),
        ('semanal', 'Semanal'),
        ('quinzenal', 'Quinzenal'),
        ('mensal', 'Mensal'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]
    
    FORMA_CALCULO_CHOICES = [
        ('price', 'Tabela Price'),
        ('sac', 'Sistema de Amortização Constante'),
        ('simple', 'Juros Simples'),
        # adicione outras formas conforme necessário
    ]
    
    descricao = models.CharField(max_length=255, unique=True)
    numero_de_prestacoes = models.IntegerField(default=1)
    periodicidade = models.CharField(max_length=20, choices=PERIODICIDADE_CHOICES)
    forma_de_calculo = models.CharField(max_length=20, choices=FORMA_CALCULO_CHOICES)
    recorencia_de_moras = models.IntegerField(default=0)
    percentual_de_juros = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        default=Decimal('0.000')
    )
    percentual_juros_de_demora = models.DecimalField(
        max_digits=5, 
        decimal_places=3, 
        default=Decimal('0.000'),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    taxa = models.ForeignKey(
        Taxa, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    ativo = models.BooleanField(default=True)
    excluir_sabados = models.BooleanField(default=True)
    excluir_domingos = models.BooleanField(default=True)
    excluir_dia_de_pag_no_sabado = models.BooleanField(default=False)
    excluir_dia_de_pag_no_domingo = models.BooleanField(default=True)
    periodo_variavel = models.IntegerField(null=True, blank=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Definição de Crédito"
        verbose_name_plural = "Definições de Crédito"
        ordering = ['descricao']
    
    def __str__(self):
        return self.descricao
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validação do percentual de juros de demora
        if self.percentual_juros_de_demora > Decimal('100.000'):
            raise ValidationError({
                'percentual_juros_de_demora': 'Percentual de juros de demora não pode ser maior que 100%'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)