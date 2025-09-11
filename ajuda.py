import requests

API_KEY = "sk-a456d860a89d489da0dfb05e27ebf3a3"  # Substitua pela sua chave API
API_URL = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def ask_deepseek_coder(mensagem, linguagem=None):
    # Preparar o contexto para o modelo de código
    system_message = "Você é um assistente especializado em programação."
    if linguagem:
        system_message += f" Especialista em {linguagem}."
    
    data = {
        "model": "deepseek-coder",  # ⭐ Modelo específico para código
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": mensagem}
        ],
        "temperature": 0.3,  # Um pouco mais baixo para respostas técnicas
        "max_tokens": 4000   # Permite respostas mais longas para código
    }
    
    response = requests.post(API_URL, json=data, headers=headers)
    return response.json()

# Exemplos de uso: