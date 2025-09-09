# creditos/serializers.py
from rest_framework import serializers
from .models import Credito, Pagamento, Parcela, Remissao
from clientes.serializers import ClienteSerializer

class RemissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remissao
        fields = '__all__'

class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = '__all__'

class PagamentoSerializer(serializers.ModelSerializer):
    parcelas = ParcelaSerializer(many=True, read_only=True)
    remissoes = RemissaoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pagamento
        fields = '__all__'

class CreditoSerializer(serializers.ModelSerializer):
    pagamentos = PagamentoSerializer(many=True, read_only=True)
    cliente_info = ClienteSerializer(source='cliente', read_only=True)
    utilizador_nome = serializers.CharField(source='utilizador.get_full_name', read_only=True)
    
    class Meta:
        model = Credito
        fields = '__all__'
        read_only_fields = ['date_created', 'last_updated', 'total_pago', 'total_moras', 'valor_em_divida']