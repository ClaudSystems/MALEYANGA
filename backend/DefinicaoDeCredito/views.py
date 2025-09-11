from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DefinicaoDeCredito
from .serializers import DefinicaoDeCreditoSerializer

class DefinicaoDeCreditoViewSet(viewsets.ModelViewSet):
    queryset = DefinicaoDeCredito.objects.all()
    serializer_class = DefinicaoDeCreditoSerializer
    
    def get_queryset(self):
        queryset = DefinicaoDeCredito.objects.all()
        
        # Filtro por status ativo
        ativo = self.request.query_params.get('ativo', None)
        if ativo is not None:
            if ativo.lower() == 'true':
                queryset = queryset.filter(ativo=True)
            elif ativo.lower() == 'false':
                queryset = queryset.filter(ativo=False)
        
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        # Soft delete - marca como inativo em vez de deletar
        instance = self.get_object()
        instance.ativo = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def reativar(self, request, pk=None):
        instance = self.get_object()
        instance.ativo = True
        instance.save()
        return Response({'status': 'reativado'})