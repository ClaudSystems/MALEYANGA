import os
import sys
import django
import requests
import json

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configura as settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MALEYANGA.settings')
django.setup()

# Agora o script pode acessar o Django
from django.contrib.auth import get_user_model

User = get_user_model()

# URL da API
url = "http://localhost:8000/api/taxas/"
data = {
    "nome": "Taxa Teste",
    "valor": 10.50,
    "tipo": "percentual",
    "descricao": "Taxa de teste"
}

print("Testando API de taxas...")

# Método 1: Teste simples sem autenticação (se você desativou a autenticação)
try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")
except Exception as e:
    print(f"Erro: {e}")

print("\n" + "="*50 + "\n")

# Método 2: Criar um usuário de teste e obter token
try:
    # Tenta criar um usuário de teste ou usar um existente
    try:
        user = User.objects.get(username="testuser")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com"
        )
        print("Usuário de teste criado")
    
    # URL para obter token JWT
    token_url = "http://localhost:8000/api/token/"
    login_data = {
        "username": "admin",
        "password": "admin2020"
    }
    
    # Obter token
    token_response = requests.post(token_url, json=login_data)
    print(f"Token status: {token_response.status_code}")
    
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get('access')
        print(f"Token obtido: {access_token[:20]}...")
        
        # Fazer requisição com token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=data, headers=headers)
        print(f"Status com token: {response.status_code}")
        print(f"Resposta com token: {response.text}")
    else:
        print(f"Falha ao obter token: {token_response.text}")
        
except Exception as e:
    print(f"Erro no método 2: {e}")