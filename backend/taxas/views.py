from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Taxa
from .serializers import TaxaSerializer

class TaxaViewSet(viewsets.ModelViewSet):
    queryset = Taxa.objects.all()
    serializer_class = TaxaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activo', 'entidade', 'recorencia']
    search_fields = ['nome', 'entidade__nome']
    ordering_fields = ['nome', 'data_criacao', 'valor']
    ordering = ['nome']
    
    def perform_create(self, serializer):
        # Associa o utilizador atual à taxa
        serializer.save(utilizador=self.request.user)
    
    def get_queryset(self):
        queryset = Taxa.objects.all()
        
        # Filtro por entidade do usuário atual (se aplicável)
        entidade_id = self.request.query_params.get('minha_entidade', None)
        if entidade_id and hasattr(self.request.user, 'entidade'):
            queryset = queryset.filter(entidade=self.request.user.entidade)
        
        # Filtro por status ativo
        activo = self.request.query_params.get('activo', None)
        if activo is not None:
            if activo.lower() == 'true':
                queryset = queryset.filter(activo=True)
            elif activo.lower() == 'false':
                queryset = queryset.filter(activo=False)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        taxas_activas = self.get_queryset().filter(activo=True)
        serializer = self.get_serializer(taxas_activas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_activo(self, request, pk=None):
        taxa = self.get_object()
        taxa.activo = not taxa.activo
        taxa.save()
        return Response({'activo': taxa.activo})