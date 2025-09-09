# credito/admin.py
from django.contrib import admin
from .models import Credito, Pagamento, Parcela, Remissao

@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    list_display = ['numero_do_credito', 'cliente', 'valor_creditado', 'estado', 'date_concecao']
    list_filter = ['estado', 'em_divida', 'em_mora']
    search_fields = ['numero_do_credito', 'cliente__nome']

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['numero_de_pagamento', 'credito', 'valor_da_prestacao', 'pago', 'data_previsto_de_pagamento']
    list_filter = ['pago', 'credito__estado']

@admin.register(Parcela)
class ParcelaAdmin(admin.ModelAdmin):
    list_display = ['numero_do_recibo', 'cliente', 'valor_parcial', 'data_de_pagamento']
    list_filter = ['forma_de_pagamento']

@admin.register(Remissao)
class RemissaoAdmin(admin.ModelAdmin):
    list_display = ['pagamento', 'valor_da_remissao', 'created_date']