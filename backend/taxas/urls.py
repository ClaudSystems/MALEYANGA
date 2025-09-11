from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaxaViewSet

router = DefaultRouter()
router.register(r'', TaxaViewSet, basename='')  # ← Registre sem prefixo

urlpatterns = [
    path('', include(router.urls)),
]