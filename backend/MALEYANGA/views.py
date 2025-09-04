from django.shortcuts import render
from django.conf import settings

def index(request):
    context = {
        'debug': settings.DEBUG,
        'vite_dev_server_url': settings.VITE_DEV_SERVER_URL if settings.DEBUG else ''
    }
    return render(request, 'base.html')  # ⭐ MUDE PARA 'base.html' (sem MALEYANGA/)