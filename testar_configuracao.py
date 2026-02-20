"""
Script de teste para validar configurações antes de executar a automação
"""
import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

print("="*60)
print("  TESTE DE CONFIGURAÇÃO - Extrator de Comentários do Bot")
print("="*60)
print()

# Testa se o arquivo .env existe
if not os.path.exists(".env"):
    print("❌ ERRO: Arquivo .env não encontrado!")
    print()
    print("Solução:")
    print("  1. Copie o arquivo .env.example para .env")
    print("  2. Edite o .env e preencha suas credenciais")
    print()
    sys.exit(1)

print("✅ Arquivo .env encontrado")

# Testa variáveis de ambiente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

errors = []

if not GITHUB_TOKEN or GITHUB_TOKEN == "seu_token_aqui":
    errors.append("GITHUB_TOKEN")
    print("❌ GITHUB_TOKEN não configurado ou inválido")
else:
    print("✅ GITHUB_TOKEN configurado")
    # Verifica formato básico
    if GITHUB_TOKEN.startswith("ghp_") or GITHUB_TOKEN.startswith("github_pat_"):
        print("   Formato: ✓ OK")
    else:
        print("   ⚠️ Aviso: Formato do token não reconhecido")

if not GITHUB_OWNER or GITHUB_OWNER == "nome_do_dono_do_repositorio":
    errors.append("GITHUB_OWNER")
    print("❌ GITHUB_OWNER não configurado")
else:
    print(f"✅ GITHUB_OWNER: {GITHUB_OWNER}")

if not GITHUB_REPO or GITHUB_REPO == "nome_do_repositorio":
    errors.append("GITHUB_REPO")
    print("❌ GITHUB_REPO não configurado")
else:
    print(f"✅ GITHUB_REPO: {GITHUB_REPO}")

print()

if errors:
    print("="*60)
    print("❌ ERROS ENCONTRADOS")
    print("="*60)
    print()
    print("Configure as seguintes variáveis no arquivo .env:")
    for var in errors:
        print(f"  - {var}")
    print()
    sys.exit(1)

# Testa conexão com a API do GitHub
print("Testando conexão com a API do GitHub...")
print()

try:
    import requests
except ImportError:
    print("❌ Módulo 'requests' não encontrado")
    print()
    print("Solução:")
    print("  Execute: pip install -r requirements.txt")
    print()
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Teste 1: Validar token
print("[1/3] Validando token...")
response = requests.get("https://api.github.com/user", headers=headers)

if response.status_code == 200:
    user = response.json()
    print(f"      ✅ Token válido! Autenticado como: {user.get('login')}")
elif response.status_code == 401:
    print("      ❌ Token inválido ou expirado")
    print()
    print("Solução:")
    print("  1. Verifique se copiou o token completo")
    print("  2. Gere um novo token: https://github.com/settings/tokens")
    sys.exit(1)
else:
    print(f"      ⚠️ Erro inesperado: {response.status_code}")
    print(f"      Resposta: {response.text}")

# Teste 2: Verificar acesso ao repositório
print(f"[2/3] Verificando acesso ao repositório {GITHUB_OWNER}/{GITHUB_REPO}...")
url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    repo_data = response.json()
    print(f"      ✅ Acesso OK: {repo_data.get('full_name')}")
    print(f"      Descrição: {repo_data.get('description', 'Sem descrição')[:60]}")
elif response.status_code == 404:
    print("      ❌ Repositório não encontrado ou sem acesso")
    print()
    print("Solução:")
    print(f"  1. Verifique se {GITHUB_OWNER}/{GITHUB_REPO} está correto")
    print("  2. Confirme se o token tem acesso a este repositório")
    print("  3. Para tokens fine-grained, adicione o repositório nas configurações")
    sys.exit(1)
elif response.status_code == 403:
    print("      ❌ Sem permissão para acessar o repositório")
    print()
    print("Solução:")
    print("  Verifique as permissões do token")
    sys.exit(1)
else:
    print(f"      ⚠️ Erro inesperado: {response.status_code}")

# Teste 3: Verificar permissão de Pull Requests
print("[3/3] Verificando permissão de leitura de Pull Requests...")
url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls"
response = requests.get(url, headers=headers, params={"per_page": 1, "state": "all"})

if response.status_code == 200:
    prs = response.json()
    if prs:
        print("      ✅ Permissão OK! Encontrados Pull Requests")
        print(f"      Exemplo: PR #{prs[0].get('number')} - {prs[0].get('title')[:40]}")
    else:
        print("      ✅ Permissão OK! (Nenhum PR encontrado no repositório)")
elif response.status_code == 404:
    print("      ⚠️ Endpoint de Pull Requests não acessível")
    print("      O repositório pode não ter PRs ou ser de um tipo especial")
elif response.status_code == 403:
    print("      ❌ Sem permissão para ler Pull Requests")
    print()
    print("Solução:")
    print("  Adicione permissão 'Pull requests - Read' ao token:")
    print("  - Fine-grained: Repository permissions → Pull requests → Read-only")
    print("  - Classic: Escopo 'repo' ou 'public_repo'")
    sys.exit(1)
else:
    print(f"      ⚠️ Erro inesperado: {response.status_code}")

# Teste de limite de API
rate_limit = response.headers.get("X-RateLimit-Remaining", "?")
rate_limit_total = response.headers.get("X-RateLimit-Limit", "?")
print()
print(f"Limite de API: {rate_limit}/{rate_limit_total} requisições restantes")

print()
print("="*60)
print("✅ TODOS OS TESTES PASSARAM!")
print("="*60)
print()
print("Você pode executar a automação agora:")
print("  python github_pr_comments_extractor.py")
print()
print("Ou no Windows:")
print("  executar.bat")
print()
