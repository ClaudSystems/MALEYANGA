from django.contrib import admin
from .models import DefinicaoDeCredito

@admin.register(DefinicaoDeCredito)
class DefinicaoDeCreditoAdmin(admin.ModelAdmin):
    list_display = [
        'descricao',
        'numero_de_prestacoes',
        'periodicidade',
        'forma_de_calculo',
        'percentual_de_juros',
        'ativo'
    ]
    list_filter = ['ativo', 'periodicidade', 'forma_de_calculo']
    search_fields = ['descricao']
    list_editable = ['ativo']