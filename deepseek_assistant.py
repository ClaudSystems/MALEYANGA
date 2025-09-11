import os
import json
import requests
from typing import List, Dict
import argparse
import sys

class DeepSeekProgrammingAssistant:
    def __init__(self, api_key: str = None, model: str = "deepseek-chat"):
        self.api_key = "sk-a456d860a89d489da0dfb05e27ebf3a3"
        if not self.api_key:
            raise ValueError("API key não encontrada. Configure a variável DEEPSEEK_API_KEY ou passe a chave como argumento.")
        
        self.model = model
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.conversation_history = []
        
        self.system_prompt = """Você é um assistente de programação especializado. Sua função é ajudar com:
1. Escrever código em várias linguagens
2. Debuggar e encontrar erros
3. Otimizar código existente
4. Explicar conceitos de programação
5. Sugerir melhores práticas
6. Converter código entre linguagens
7. Gerar documentação

Forneça respostas claras, código bem formatado e explicações concisas.
Use markdown para formatar código e destacar pontos importantes."""

    def send_message(self, message: str, max_tokens: int = 2000) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        messages.extend(self.conversation_history[-6:])
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            assistant_reply = result['choices'][0]['message']['content']
            
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_reply})
            
            return assistant_reply
            
        except requests.exceptions.RequestException as e:
            return f"Erro na requisição: {e}"
        except KeyError as e:
            return f"Erro ao processar resposta da API: {e}"

    def clear_history(self):
        self.conversation_history = []

    def analyze_code(self, code: str, language: str) -> str:
        prompt = f"Analise este código {language}:\n\n```{language}\n{code}\n```\n\nPor favor:\n1. Identifique possíveis erros ou problemas\n2. Sugira melhorias\n3. Explique o que o código faz\n4. Se houver erros, mostre como corrigir"
        return self.send_message(prompt)

    def generate_code(self, description: str, language: str = "python") -> str:
        prompt = f"Gere código {language} para:\n\n{description}\n\nPor favor:\n1. Forneça o código completo e funcional\n2. Inclua comentários explicativos\n3. Use boas práticas da linguagem\n4. Explique brevemente a solução"
        return self.send_message(prompt)

    def debug_code(self, code: str, error: str, language: str) -> str:
        prompt = f"Debug este código {language}:\n\n```{language}\n{code}\n```\n\nErro encontrado:\n{error}\n\nPor favor:\n1. Identifique a causa do erro\n2. Mostre o código corrigido\n3. Explique a correção"
        return self.send_message(prompt)

def main():
    parser = argparse.ArgumentParser(description="Assistente de Programação DeepSeek")
    parser.add_argument("--api-key", help="Chave da API DeepSeek")
    parser.add_argument("--analyze", help="Arquivo para análise")
    parser.add_argument("--generate", help="Descrição do código a ser gerado")
    parser.add_argument("--language", default="python", help="Linguagem de programação")
    parser.add_argument("--debug", nargs=2, help="Arquivo e mensagem de erro para debug")
    
    args = parser.parse_args()
    
    try:
        assistant = DeepSeekProgrammingAssistant(api_key=args.api_key)
        
        if args.analyze:
            with open(args.analyze, 'r', encoding='utf-8') as f:
                code = f.read()
            result = assistant.analyze_code(code, args.language)
            print("\n" + "="*50)
            print("ANÁLISE DE CÓDIGO:")
            print("="*50)
            print(result)
            
        elif args.generate:
            result = assistant.generate_code(args.generate, args.language)
            print("\n" + "="*50)
            print("CÓDIGO GERADO:")
            print("="*50)
            print(result)
            
        elif args.debug:
            file_path, error_msg = args.debug
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            result = assistant.debug_code(code, error_msg, args.language)
            print("\n" + "="*50)
            print("DEBUG:")
            print("="*50)
            print(result)
            
        else:
            print("DeepSeek Programming Assistant")
            print("Digite 'quit' para sair ou 'clear' para limpar histórico")
            print("-" * 50)
            
            while True:
                user_input = input("\nVocê: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'sair']:
                    break
                elif user_input.lower() in ['clear', 'limpar']:
                    assistant.clear_history()
                    print("Histórico limpo!")
                    continue
                elif not user_input:
                    continue
                
                response = assistant.send_message(user_input)
                print(f"\nAssistente: {response}")
                
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()