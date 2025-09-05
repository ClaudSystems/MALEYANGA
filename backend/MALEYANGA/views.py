from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import json

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid credentials'
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Server error: ' + str(e)
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPI(View):
    def post(self, request):
        try:
            logout(request)
            return JsonResponse({
                'success': True,
                'message': 'Logout successful'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Server error: ' + str(e)
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class CheckAuthAPI(View):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email
                }
            })
        else:
            return JsonResponse({
                'authenticated': False,
                'message': 'User not authenticated'
            })

def index(request):
    context = {
        'debug': settings.DEBUG,
        'vite_dev_server_url': settings.VITE_DEV_SERVER_URL if hasattr(settings, 'VITE_DEV_SERVER_URL') and settings.DEBUG else '',
        'vite_dev_mode': settings.DEBUG
    }
    return render(request, 'base.html', context)

# View protegida de exemplo
@login_required
def protected_view(request):
    return JsonResponse({
        'message': 'This is a protected view',
        'user': {
            'id': request.user.id,
            'username': request.user.username
        }
    })

# API view usando decorators do REST framework
@csrf_exempt
def api_login(request):
    """Alternative API view for login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login realizado com sucesso',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Credenciais inválidas'
                }, status=401)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Dados JSON inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro no servidor: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido'
    }, status=405)
@login_required
def home_page(request):
    """
    Renderiza a homepage principal.
    A interface de utilizador é gerida pelo React,
    que será carregado através do template.
    """
    return render(request, 'home.html')