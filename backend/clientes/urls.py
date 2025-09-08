from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, AssinanteViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'assinantes', AssinanteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
