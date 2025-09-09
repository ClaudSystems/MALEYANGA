# feriado/models.py
from django.db import models

class Feriado(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField(unique=True)
    descricao = models.TextField(blank=True, null=True)
    recorrente = models.BooleanField(default=True)

    class Meta:
        ordering = ['data']
        verbose_name_plural = 'Feriados'

    def __str__(self):
        return f"{self.nome} ({self.data})"