"""
Script simplificado para extrair comentários de um PR específico
Uso: python extrair_pr_especifico.py [numero_do_pr]
"""
import sys
import os
from dotenv import load_dotenv
from github_pr_comments_extractor import GitHubPRCommentsExtractor

# Carrega variáveis do .env
load_dotenv()

# Configurações
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
BOT_USERNAME = os.getenv("BOT_USERNAME")
DISABLE_SSL_VERIFY = os.getenv("DISABLE_SSL_VERIFY", "false").lower() == "true"

# Validação
if not all([GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO]):
    print("❌ ERRO: Configure as variáveis no arquivo .env")
    sys.exit(1)

# Obtém número do PR
if len(sys.argv) > 1:
    try:
        pr_number = int(sys.argv[1])
    except ValueError:
        print("❌ ERRO: Número de PR inválido")
        print("Uso: python extrair_pr_especifico.py [numero_do_pr]")
        sys.exit(1)
else:
    pr_input = input("Digite o número do Pull Request: ").strip()
    try:
        pr_number = int(pr_input)
    except ValueError:
        print("❌ ERRO: Número inválido")
        sys.exit(1)

# Cria o extrator
extractor = GitHubPRCommentsExtractor(
    token=GITHUB_TOKEN,
    owner=GITHUB_OWNER,
    repo=GITHUB_REPO,
    bot_username=BOT_USERNAME,
    verify_ssl=not DISABLE_SSL_VERIFY
)

print("="*60)
print(f"EXTRAINDO COMENTÁRIOS DO PR #{pr_number}")
print("="*60)
print(f"🤖 Bot: {extractor.bot_username}*")
print()

# Extrai comentários (formato filtrado com apenas 4 campos)
comments = extractor.extract_all_bot_comments(specific_pr=pr_number, filtered=True)

# Salva resultado
if comments:
    output_file = f"bot_comments_PR{pr_number}.json"
    extractor.save_to_json(comments, output_file, filtered=True)
    print()
    print("="*60)
    print("✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
else:
    print()
    print("="*60)
    print("⚠️ NENHUM COMENTÁRIO ENCONTRADO")
    print("="*60)
    print()
    print("Possíveis motivos:")
    print("  - O bot não comentou neste PR")
    print("  - O nome do bot está incorreto")
    print("  - PR não possui comentários de revisão")
