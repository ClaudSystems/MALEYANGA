# credito/models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Credito(models.Model):
    ESTADO_CHOICES = [
        ('Aberto', 'Aberto'),
        ('Pendente', 'Pendente'),
        ('Fechado', 'Fechado'),
        ('EmProgresso', 'Em Progresso'),
    ]
    
    PERIODICIDADE_CHOICES = [
        ('mensal', 'Mensal'),
        ('quinzenal', 'Quinzenal'),
        ('semanal', 'Semanal'),
        ('diario', 'Diário'),
        ('doisdias', 'Dois Dias'),
        ('variavel', 'Variável'),
    ]
    
    FORMA_CALCULO_CHOICES = [
        ('pmt', 'PMT'),
        ('taxafixa', 'Taxa Fixa'),
    ]
    
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    utilizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    valor_creditado = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    date_concecao = models.DateField()
    moras = models.IntegerField(default=0)
    validade = models.DateField(null=True, blank=True)
    numero_do_credito = models.CharField(max_length=50)
    percentual_de_juros = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    percentual_juros_de_demora = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal('0.000'))
    total_da_divida_sem_moras = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    valor_em_divida = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    total_pago = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    total_moras = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    taxas = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Aberto')
    forma_de_calculo = models.CharField(max_length=20, choices=FORMA_CALCULO_CHOICES)
    periodicidade = models.CharField(max_length=20, choices=PERIODICIDADE_CHOICES)
    em_divida = models.BooleanField(default=True)
    invalido = models.BooleanField(default=False)
    numero_de_prestacoes = models.IntegerField(validators=[MinValueValidator(1)])
    recorencia_de_moras = models.IntegerField(null=True, blank=True)
    reter_capital = models.BooleanField(default=False)
    valor_de_juros = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    em_mora = models.BooleanField(default=False)
    periodo_variavel = models.IntegerField(null=True, blank=True)
    ignorar_valor_pago_no_prazo = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Crédito'
        verbose_name_plural = 'Créditos'

    def __str__(self):
        return f"Crédito #{self.numero_do_credito} - {self.cliente.nome}"

    def calcular_total_pago(self):
        total = self.pagamentos.aggregate(
            total=models.Sum('valor_pago')
        )['total'] or Decimal('0.00')
        self.total_pago = total
        return total

    def calcular_total_moras(self):
        total = self.pagamentos.aggregate(
            total=models.Sum('valor_de_juros_de_demora')
        )['total'] or Decimal('0.00')
        self.total_moras = total
        return total

    def calcular_valor_em_divida(self):
        total = Decimal('0.00')
        for pagamento in self.pagamentos.all():
            total += pagamento.calcular_saldo_devido()
        self.valor_em_divida = total
        return total

    def atualizar_estado(self):
        pagamentos = self.pagamentos.all()
        
        if not self.em_divida:
            self.estado = 'Fechado'
        elif pagamentos.filter(dias_de_mora__gt=0, pago=False).exists():
            self.estado = 'Pendente'
        elif pagamentos.filter(pago=True).exists():
            self.estado = 'EmProgresso'
        else:
            self.estado = 'Aberto'
        
        self.em_mora = pagamentos.filter(dias_de_mora__gt=0, pago=False).exists()

    def clean(self):
        super().clean()
        
        if self.percentual_de_juros > Decimal('50.00'):
            raise ValidationError({'percentual_de_juros': 'Taxa de juros muito alta'})
        
        if self.percentual_juros_de_demora > Decimal('5.000'):
            raise ValidationError({'percentual_juros_de_demora': 'Taxa de mora muito alta'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Pagamento(models.Model):
    credito = models.ForeignKey(Credito, on_delete=models.CASCADE, related_name='pagamentos')
    descricao = models.CharField(max_length=200)
    numero_de_pagamento = models.CharField(max_length=50, null=True, blank=True)
    valor_da_prestacao = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    valor_de_juros = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    valor_pago_juros = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    valor_de_amortizacao = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    valor_pago_amortizacao = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    saldo_devedor = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    total_pago = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    total_pago_no_prazo = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    total_em_divida = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    total_em_divida_sem_moras = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    valor_de_juros_de_demora = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    valor_pago_demora = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    valor_da_remissao = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    dias_de_mora = models.IntegerField(default=0)
    recorencia_de_moras = models.IntegerField(default=1)
    pago = models.BooleanField(default=False)
    valores_alocados = models.BooleanField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    data_de_pagamento = models.DateField(null=True, blank=True)
    data_previsto_de_pagamento = models.DateField(null=True, blank=True)
    data_da_criacao = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['data_previsto_de_pagamento']
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f"Pagamento #{self.numero_de_pagamento or self.id} - {self.descricao}"

    def calcular_valor_pago(self):
        total = self.parcelas.aggregate(
            total=models.Sum('valor_parcial')
        )['total'] or Decimal('0.00')
        self.valor_pago = total
        return total

    def calcular_valor_remissao(self):
        total = self.remissoes.aggregate(
            total=models.Sum('valor_da_remissao')
        )['total'] or Decimal('0.00')
        self.valor_da_remissao = total
        return total

    def calcular_valor_total_devido(self):
        return (self.valor_da_prestacao + 
                (self.valor_de_juros_de_demora or Decimal('0.00')) - 
                (self.valor_da_remissao or Decimal('0.00')))

    def calcular_saldo_devido(self):
        return self.calcular_valor_total_devido() - (self.valor_pago or Decimal('0.00'))

class Parcela(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('transferencia', 'Transferência'),
        ('cheque', 'Cheque'),
        ('mbway', 'MBWay'),
        ('multibanco', 'Multibanco'),
    ]
    
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, related_name='parcelas', null=True, blank=True)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    numero_do_recibo = models.CharField(max_length=50, null=True, blank=True)
    valor_parcial = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    valor_pago_backup = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    data_de_pagamento = models.DateField()
    utilizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.SET_NULL, null=True, blank=True)
    nome_do_cliente = models.CharField(max_length=200, default="")
    forma_de_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    invalido = models.BooleanField(null=True, blank=True)

    class Meta:
        ordering = ['-data_de_pagamento']
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'

    def __str__(self):
        return f"Parcela #{self.id} - {self.valor_parcial}€"

    def save(self, *args, **kwargs):
        if self.pagamento and not self.nome_do_cliente:
            self.nome_do_cliente = self.pagamento.credito.cliente.nome
        if not self.cliente and self.pagamento:
            self.cliente = self.pagamento.credito.cliente
        super().save(*args, **kwargs)

class Remissao(models.Model):
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, related_name='remissoes')
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor_da_remissao = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    percentual = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    utilizador = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Remissão'
        verbose_name_plural = 'Remissões'

    def __str__(self):
        return f"Remissão #{self.id} - {self.valor_da_remissao}€"

    def save(self, *args, **kwargs):
        if self.valor_da_remissao > 0 and self.pagamento.valor_da_prestacao > 0:
            self.percentual = (self.valor_da_remissao / self.pagamento.valor_da_prestacao * 100)
        super().save(*args, **kwargs)