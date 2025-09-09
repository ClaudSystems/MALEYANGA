# clientes/apps.py (deve estar assim)
from django.apps import AppConfig

class ClientesConfig(AppConfig):  # ← Nome da classe
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'  # ← Nome da app
    verbose_name = 'Clientes'