import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MALEYANGA.settings')
django.setup()

from django.contrib.auth.models import User

# Lista de usuários para criar
users_to_create = [
    {'username': 'admin', 'password': 'admin2020', 'email': 'admin@example.com'},
    {'username': 'user', 'password': 'user2020', 'email': 'user@example.com'},
]

for user_data in users_to_create:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            email=user_data['email']
        )
        print(f"✅ Usuário criado: {user.username}")
    else:
        print(f"⚠️  Usuário já existe: {user_data['username']}")

print("🎉 Processo concluído!")