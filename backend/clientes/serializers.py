from rest_framework import serializers
from .models import Cliente, Assinante

class ClienteSerializer(serializers.ModelSerializer):
    assinantes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Assinante.objects.all(),
        required=False,
        allow_empty=True,
        default=list
    )

    class Meta:
        model = Cliente
        fields = '__all__'

class AssinanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assinante
        fields = '__all__'
