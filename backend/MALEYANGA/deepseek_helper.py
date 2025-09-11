import os
import subprocess
import requests
import json

class DeepSeekCodeAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Configure a variável de ambiente DEEPSEEK_API_KEY")
        
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_code(self, code, task="analyze"):
        """Analisa código usando o DeepSeek API v1"""
        prompts = {
            "analyze": "Analise este código Python, identifique problemas e sugira melhorias:",
            "explain": "Explique este código Python em detalhes:",
            "optimize": "Otimize este código Python e explique as melhorias:",
            "debug": "Procure bugs ou problemas neste código Python:",
            "review": "Faça um code review detalhado deste código:"
        }
        
        prompt = prompts.get(task, prompts["analyze"])
        
        payload = {
            "model": "deepseek-coder",
            "messages": [
                {
                    "role": "system", 
                    "content": "Você é um especialista em Python e análise de código. Forneça respostas úteis e detalhadas."
                },
                {
                    "role": "user",
                    "content": f"{prompt}\n\n```python\n{code}\n```"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Erro na API: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Erro ao conectar com DeepSeek: {str(e)}"

def get_selected_code():
    """Tenta obter código selecionado no VS Code"""
    try:
        # Método para VS Code
        result = subprocess.run([
            'code', '--get-selected-text'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
        
        # Se não conseguir, retorna None
        return None
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None

def read_example_code():
    """Código de exemplo para teste"""
    return """
# Exemplo de código para análise
def calcular_media(numeros):
    soma = 0
    for i in range(len(numeros)):
        soma += numeros[i]
    return soma / len(numeros)

def encontrar_maximo(lista):
    max_val = lista[0]
    for item in lista:
        if item > max_val:
            max_val = item
    return max_val

nums = [1, 2, 3, 4, 5]
print("Média:", calcular_media(nums))
print("Máximo:", encontrar_maximo(nums))
"""

if __name__ == "__main__":
    import sys
    
    print("🤖 DeepSeek Code Analyzer v1.x")
    print("=" * 50)
    
    # Tentar obter código selecionado
    selected_code = get_selected_code()
    
    if selected_code:
        print("📝 Código selecionado detectado!")
        code_to_analyze = selected_code
    else:
        print("⚠️  Nenhum código selecionado. Usando exemplo...")
        code_to_analyze = read_example_code()
        print("\nExemplo usado:")
        print("=" * 30)
        print(code_to_analyze)
        print("=" * 30)
    
    # Menu de opções
    print("\n🔧 Escolha o tipo de análise:")
    print("1. Análise geral")
    print("2. Explicação detalhada")
    print("3. Otimização")
    print("4. Debug")
    print("5. Code Review")
    
    choice = input("\nDigite sua escolha (1-5, padrão=1): ").strip()
    
    options = {
        "1": "analyze",
        "2": "explain", 
        "3": "optimize",
        "4": "debug",
        "5": "review"
    }
    
    analysis_type = options.get(choice, "analyze")
    
    # Analisar o código
    try:
        analyzer = DeepSeekCodeAnalyzer()
        print(f"\n🔄 Analisando com DeepSeek ({analysis_type})...")
        print("⏳ Isso pode levar alguns segundos...\n")
        
        result = analyzer.analyze_code(code_to_analyze, analysis_type)
        
        print("=" * 60)
        print("🔍 RESULTADO DA ANÁLISE")
        print("=" * 60)
        print(result)
        print("=" * 60)
        
        # Salvar resultado em arquivo
        with open("deepseek_analysis.txt", "w", encoding="utf-8") as f:
            f.write(f"Análise tipo: {analysis_type}\n")
            f.write(f"Código analisado:\n{code_to_analyze}\n\n")
            f.write("Resultado:\n")
            f.write(result)
        
        print("\n💾 Resultado salvo em 'deepseek_analysis.txt'")
        
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        print("👉 Crie um arquivo .env com: DEEPSEEK_API_KEY=sua_chave_aqui")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    input("\nPressione Enter para sair...")