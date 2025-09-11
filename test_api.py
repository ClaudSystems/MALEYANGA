import os
from dotenv import load_dotenv
import requests
import json

# Carregar variáveis do .env
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

def test_connection():
    if not API_KEY:
        print("❌ API_KEY não encontrada no arquivo .env")
        print("👉 Adicione: DEEPSEEK_API_KEY=sua_chave_real_aqui")
        return False
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-coder",
        "messages": [
            {"role": "user", "content": "Olá! Isso é um teste de conexão. Responda com 'Conexão bem-sucedida!'"}
        ],
        "max_tokens": 50
    }
    
    try:
        print("🔗 Testando conexão com DeepSeek API...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Conexão bem-sucedida!")
            print("📝 Resposta:", result['choices'][0]['message']['content'])
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print("📋 Detalhes:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

if __name__ == "__main__":
    test_connection()
