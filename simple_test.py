import os
import requests

# CONFIGURAÇÃO MANUAL - COLE SUA CHAVE AQUI ↓
DEEPSEEK_API_KEY = "sk-sk-ccfe524c5294438ea0ef9d9411159ce1"  # 👈 COLE SUA CHAVE VERDADEIRA AQUI!

def test_connection():
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "sk-sk-ccfe524c5294438ea0ef9d9411159ce1":
        print("❌ API_KEY não configurada!")
        print("👉 Edite este arquivo e cole sua chave real da DeepSeek")
        return False
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-coder",
        "messages": [
            {"role": "user", "content": "Teste de conexão. Responda com 'OK!'"}
        ],
        "max_tokens": 50
    }
    
    try:
        print("🔗 Testando conexão com DeepSeek API...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Conexão bem-sucedida!")
            print("📝 Resposta:", result['choices'][0]['message']['content'])
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print("📋 Detalhes:", response.text[:200])
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

if __name__ == "__main__":
    test_connection()
