import os
import requests
import subprocess

# ================= CONFIGURAÇÃO =================
# COLE SUA CHAVE API AQUI DIRETAMENTE:
DEEPSEEK_API_KEY = "sk-a456d860a89d489da0dfb05e27ebf3a3"
# ================================================

class DeepSeekCodeAgent:
    def __init__(self, api_key: str = None):
        # Usa a chave do arquivo se não for passada como parâmetro
        self.api_key = api_key or DEEPSEEK_API_KEY
        if self.api_key == "cole_sua_chave_aqui" or not self.api_key:
            raise ValueError("Por favor, cole sua chave API no início do arquivo!")
        
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.current_directory = os.getcwd()

    def call_deepseek(self, message: str) -> str:
        """Faz chamada para API do DeepSeek"""
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Erro na API: {str(e)}"

    def read_file(self, file_path: str) -> str:
        """Lê conteúdo de um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"

    def write_file(self, file_path: str, content: str) -> str:
        """Escreve conteúdo em um arquivo"""
        try:
            # Cria diretórios se não existirem
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Arquivo {file_path} salvo com sucesso!"
        except Exception as e:
            return f"❌ Erro ao escrever arquivo: {str(e)}"

    def list_files(self, directory: str = None) -> str:
        """Lista arquivos no diretório"""
        target_dir = directory or self.current_directory
        try:
            files = []
            for item in os.listdir(target_dir):
                full_path = os.path.join(target_dir, item)
                if os.path.isfile(full_path):
                    files.append(f"📄 {item}")
                else:
                    files.append(f"📁 {item}/")
            return "\n".join(files) if files else "📂 Diretório vazio"
        except Exception as e:
            return f"❌ Erro ao listar arquivos: {str(e)}"

    def execute_command(self, command: str) -> str:
        """Executa comando no sistema"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.current_directory)
            if result.returncode == 0:
                return f"✅ Comando executado:\n{result.stdout}"
            else:
                return f"❌ Erro no comando:\n{result.stderr}"
        except Exception as e:
            return f"❌ Erro ao executar comando: {str(e)}"

    def process_user_request(self, user_input: str):
        """Processa solicitação do usuário"""
        
        # Comandos especiais
        if user_input.startswith("!list"):
            path = user_input[5:].strip() or "."
            return self.list_files(path)
        
        elif user_input.startswith("!read "):
            file_path = user_input[6:].strip()
            content = self.read_file(file_path)
            return f"📖 Conteúdo de {file_path}:\n\n{content}"
        
        elif user_input.startswith("!run "):
            command = user_input[5:].strip()
            return self.execute_command(command)
        
        elif user_input.startswith("!cd "):
            new_dir = user_input[4:].strip()
            try:
                os.chdir(new_dir)
                self.current_directory = os.getcwd()
                return f"📁 Diretório alterado para: {self.current_directory}"
            except Exception as e:
                return f"❌ Erro ao mudar diretório: {str(e)}"
        
        elif user_input.startswith("!write "):
            # Formato: !write arquivo.txt conteúdo do arquivo
            parts = user_input[7:].split(' ', 1)
            if len(parts) == 2:
                file_path, content = parts
                return self.write_file(file_path.strip(), content.strip())
            else:
                return "❌ Uso: !write <arquivo> <conteúdo>"
        
        elif user_input.startswith("!create "):
            # Cria arquivo com conteúdo do DeepSeek
            file_path = user_input[8:].strip()
            prompt = f"Crie um código para o arquivo {file_path}. Forneça apenas o código sem explicações."
            code = self.call_deepseek(prompt)
            return self.write_file(file_path, code)
        
        # Consulta normal ao DeepSeek
        return self.call_deepseek(user_input)

def main():
    try:
        agent = DeepSeekCodeAgent()
        
        print("🤖 DeepSeek Code Agent Ativado!")
        print("📍 Diretório atual:", agent.current_directory)
        print("🔑 API Key configurada:", agent.api_key[:10] + "..." if agent.api_key else "Não configurada")
        print("\n💡 Comandos disponíveis:")
        print("  !list [dir]       - Lista arquivos")
        print("  !read <arquivo>   - Lê arquivo")
        print("  !run <comando>    - Executa comando")
        print("  !cd <diretório>   - Muda diretório")
        print("  !write <arq> <cont> - Escreve arquivo")
        print("  !create <arquivo> - Cria arquivo com IA")
        print("  quit              - Sair")
        print("\n" + "="*60)
        
        while True:
            try:
                user_input = input("\n🎯 Sua solicitação: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'sair']:
                    print("👋 Até logo!")
                    break
                
                if not user_input:
                    continue
                
                # Processa a solicitação
                result = agent.process_user_request(user_input)
                print(f"\n{'='*50}")
                print(f"🤖 RESULTADO:")
                print(f"{'='*50}")
                print(result)
                print(f"{'='*50}")
                
            except KeyboardInterrupt:
                print("\n👋 Encerrado pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")
                
    except ValueError as e:
        print(f"❌ {e}")
        print("\n📝 INSTRUÇÕES:")
        print("1. Abra o arquivo deepseek_coder_agent.py")
        print("2. Localize a linha: DEEPSEEK_API_KEY = 'cole_sua_chave_aqui'")
        print("3. Substitua 'cole_sua_chave_aqui' pela sua chave real")
        print("4. Salve o arquivo e execute novamente")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()