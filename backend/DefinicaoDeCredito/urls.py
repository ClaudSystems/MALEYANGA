from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DefinicaoDeCreditoViewSet

router = DefaultRouter()
router.register(r'definicoes-credito', DefinicaoDeCreditoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]