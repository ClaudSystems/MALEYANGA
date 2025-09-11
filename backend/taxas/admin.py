from django.contrib import admin
from .models import Taxa

@admin.register(Taxa)
class TaxaAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 
        'valor', 
        'activo',
        'data_criacao'  # ⭐ Use apenas campos que EXISTEM
    ]
    list_filter = ['activo']  # ⭐ Apenas campos que existem
    search_fields = ['nome']  # ⭐ Remova 'entidade__nome' se não existir
    list_editable = ['activo']
    readonly_fields = ['data_criacao']  # ⭐ Remova 'data_atualizacao' se não existir