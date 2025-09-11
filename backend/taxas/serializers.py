from rest_framework import serializers
from .models import Taxa

class TaxaSerializer(serializers.ModelSerializer):
    entidade_nome = serializers.CharField(source='entidade.nome', read_only=True)
    utilizador_nome = serializers.CharField(source='utilizador.get_full_name', read_only=True)
    
    class Meta:
        model = Taxa
        fields = [
            'id',
            'nome',
            'valor',
            'percentagem',
            'activo',
            'entidade',
            'entidade_nome',
            'valor_minimo',
            'valor_maximo',
            'recorencia',
            'utilizador',
            'utilizador_nome',
            'data_criacao',
            'data_atualizacao'
        ]
        extra_kwargs = {
            'entidade': {'write_only': True},
            'utilizador': {'write_only': True, 'required': False}
        }
    
    def validate_percentagem(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Percentagem deve estar entre 0 e 100")
        return value
    
    def validate(self, data):
        # Validação cruzada entre valor mínimo e máximo
        valor_minimo = data.get('valor_minimo')
        valor_maximo = data.get('valor_maximo')
        
        if valor_minimo and valor_maximo and valor_minimo > valor_maximo:
            raise serializers.ValidationError({
                'valor_minimo': 'Valor mínimo não pode ser maior que valor máximo'
            })
        
        return data