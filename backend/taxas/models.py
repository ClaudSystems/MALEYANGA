from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Taxa(models.Model):
    RECORENCIA_CHOICES = [
        ('diaria', 'Diária'),
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
        ('unica', 'Única'),
    ]
    
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        null=True,
        blank=True
    )
    percentagem = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    activo = models.BooleanField(default=True)
   
    valor_minimo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True,
        blank=True
    )
    valor_maximo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True,
        blank=True
    )
    recorencia = models.CharField(
        max_length=20, 
        choices=RECORENCIA_CHOICES,
        null=True,
        blank=True
    )
        
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Taxa"
        verbose_name_plural = "Taxas"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validação personalizada
        if self.valor_minimo and self.valor_maximo:
            if self.valor_minimo > self.valor_maximo:
                raise ValidationError({
                    'valor_minimo': 'Valor mínimo não pode ser maior que valor máximo'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)