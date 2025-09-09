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
    path('', views.index, name='index'),  # ⭐ Sua view principal
    path('api/login/', views.LoginAPI.as_view(), name='api_login'),  # ⭐ API login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.home_page, name='home'),
    path('api/', include('clientes.urls')),
    path('api/', include('creditos.urls')),
]