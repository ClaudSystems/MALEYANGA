from rest_framework import serializers
from .models import DefinicaoDeCredito
from taxa.serializers import TaxaSerializer  # Ajuste conforme sua estrutura

class DefinicaoDeCreditoSerializer(serializers.ModelSerializer):
    taxa = TaxaSerializer(read_only=True)
    taxa_id = serializers.PrimaryKeyRelatedField(
        queryset=Taxa.objects.all(),
        source='taxa',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = DefinicaoDeCredito
        fields = [
            'id',
            'descricao',
            'numero_de_prestacoes',
            'periodicidade',
            'forma_de_calculo',
            'recorencia_de_moras',
            'percentual_de_juros',
            'percentual_juros_de_demora',
            'taxa',
            'taxa_id',
            'ativo',
            'excluir_sabados',
            'excluir_domingos',
            'excluir_dia_de_pag_no_sabado',
            'excluir_dia_de_pag_no_domingo',
            'periodo_variavel',
            'data_criacao',
            'data_atualizacao'
        ]
    
    def validate_percentual_juros_de_demora(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Percentual deve estar entre 0 e 100")
        return value