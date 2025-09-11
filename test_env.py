import os
from dotenv import load_dotenv

print("📁 Diretório atual:", os.getcwd())
print("📋 Arquivos na pasta:")
for file in os.listdir('.'):
    print(f"  - {file}")

# Tentar carregar .env
load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY')
print(f"🔑 API_KEY lida: {api_key}")

if api_key:
    print("✅ .env carregado com sucesso!")
else:
    print("❌ Não foi possível carregar a API_KEY do .env")
