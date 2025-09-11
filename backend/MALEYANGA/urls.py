"""
URL configuration for MALEYANGA project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ⭐ Rota principal (mantenha apenas uma)
    path('', views.home_page, name='home'),
    
    # ⭐ APIs de autenticação
    path('api/login/', views.LoginAPI.as_view(), name='api_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # ⭐ Inclua as URLs das apps - ORDEM IMPORTA!
    # Coloque rotas mais específicas primeiro
    path('api/taxas/', include('taxas.urls')),  # ⭐← ADICIONE ESTA LINHA
    path('api/clientes/', include('clientes.urls')),
    path('api/creditos/', include('creditos.urls')),
]