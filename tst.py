from flask import Flask, request, jsonify
from github import Github
import git
import os

# Configurações do GitHub e repositório
GITHUB_API_TOKEN = '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'  # Substitua pelo seu token de acesso pessoal do GitHub
REPO_NAME = 'REM-Infotech/CrawJUD-Web'  # Nome do repositório, no formato 'dono/repo'
LOCAL_REPO_PATH = 'c:\\CrawJUD-Web'  # Caminho local onde o repositório está clonado

# Monta a URL com o token para autenticação
repo_url = f'https://{GITHUB_API_TOKEN}@github.com/{REPO_NAME}.git'

if not os.path.exists(LOCAL_REPO_PATH):
    os.makedirs(LOCAL_REPO_PATH, exist_ok=True)


# Inicializa o Flask
app = Flask(__name__)
g = Github(GITHUB_API_TOKEN)


# Função para atualizar para a tag da nova release
def checkout_release_tag(tag_: str):
    try:
        # Abre o repositório local
        
        walking = list(os.walk(os.path.join(LOCAL_REPO_PATH)))
        if len(walking) == 0:
            git.Repo.clone_from(repo_url, LOCAL_REPO_PATH)
            
        repo = git.Repo(LOCAL_REPO_PATH)
        
        # Busca e alterna para a tag da nova release
        repo.git.fetch("--all", "--tags")
        repo.git.checkout(f"{tag_}")
        
        print(f"Atualizado para a tag: {tag_}")
        
    except Exception as e:
        print(f"Erro ao atualizar para a tag {tag_}: {e}")


# Endpoint para o webhook
@app.route('/webhook', methods=['POST'])
def github_webhook():
    
    data = request.json
    
    for key, value in data.items():
        
        if type(value) is dict:
            for key, value in data.items():
                print(f"Key: {key}, Value: {value}")
                
        elif type(value) is not dict:
            print(f"Key: {key}, Value: {value}")
    
    
    # Verifica se é uma nova release
    ref = data.get("ref")
    
    base_refs = ["refs/heads/Produção", "refs/heads/Homologação", "refs/heads/Master"]
    
    try:
        
        if ref and any(ref != bases for bases in base_refs):
            
            # Alterna para a tag da nova release
            checkout_release_tag(ref)

            return jsonify({"message": "Release processada e atualizada"}), 200
        
    except Exception:

        return jsonify({"message": "Evento ignorado"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
