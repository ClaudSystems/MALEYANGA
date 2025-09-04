from pathlib import Path
import os

print("🚨 DIAGNÓSTICO DE EMERGÊNCIA 🚨")

# Todos os caminhos possíveis
correct_path = Path(r'W:\projects\MALEYANGA')
print(f"1. Caminho correto: {correct_path}")
print(f"   Template: {correct_path / 'templates' / 'base.html'}")
print(f"   Existe: {(correct_path / 'templates' / 'base.html').exists()}")

# Verifica se o arquivo realmente existe
template_path = r'W:\projects\MALEYANGA\templates\base.html'
print(f"2. Caminho absoluto: {template_path}")
print(f"   Existe: {os.path.exists(template_path)}")

# Lista o conteúdo da pasta templates
templates_dir = r'W:\projects\MALEYANGA\templates'
if os.path.exists(templates_dir):
    print(f"3. Conteúdo de {templates_dir}:")
    for item in os.listdir(templates_dir):
        print(f"   - {item}")
else:
    print(f"3. ❌ PASTA {templates_dir} NÃO EXISTE!")

# Verifica permissões
print(f"4. Posso acessar?: {os.access(template_path, os.R_OK)}")