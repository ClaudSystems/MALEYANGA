# credito/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreditoViewSet, PagamentoViewSet, ParcelaViewSet, RemissaoViewSet

router = DefaultRouter()
router.register(r'creditos', CreditoViewSet)
router.register(r'pagamentos', PagamentoViewSet)
router.register(r'parcelas', ParcelaViewSet)
router.register(r'remissoes', RemissaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]