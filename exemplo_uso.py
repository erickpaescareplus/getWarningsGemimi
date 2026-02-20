"""
Exemplo de uso da classe GitHubPRCommentsExtractor
"""
from github_pr_comments_extractor import GitHubPRCommentsExtractor
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Configurações
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# Cria o extrator
extractor = GitHubPRCommentsExtractor(
    token=GITHUB_TOKEN,
    owner=GITHUB_OWNER,
    repo=GITHUB_REPO
)

# Exemplo 1: Extrair comentários de um PR específico
print("\n=== Exemplo 1: Buscar comentários de um PR específico ===")
pr_number = 123  # Altere para o número do PR que deseja testar
comments = extractor.get_pr_review_comments(pr_number)
bot_comments = extractor.filter_bot_comments(comments)

print(f"Total de comentários: {len(comments)}")
print(f"Comentários do bot: {len(bot_comments)}")

if bot_comments:
    print("\nPrimeiro comentário do bot:")
    first_comment = bot_comments[0]
    print(f"  Arquivo: {first_comment.get('path')}")
    print(f"  Linha: {first_comment.get('line')}")
    print(f"  Comentário: {first_comment.get('body')[:100]}...")

# Exemplo 2: Extrair todos os comentários (limitado a 5 PRs para teste)
print("\n\n=== Exemplo 2: Extrair de múltiplos PRs (limitado a 5) ===")
all_comments = extractor.extract_all_bot_comments(max_prs=5)

print(f"\nTotal de comentários do bot encontrados: {len(all_comments)}")

# Exemplo 2b: Extrair comentários de um PR específico (formato filtrado)
print("\n\n=== Exemplo 2b: Extrair de um PR específico (FILTRADO) ===")
specific_pr_number = 123  # Altere para o número do PR que deseja
specific_comments = extractor.extract_all_bot_comments(specific_pr=specific_pr_number, filtered=True)

print(f"\nTotal de comentários do bot no PR #{specific_pr_number}: {len(specific_comments)}")
if specific_comments:
    print("\nPrimeiro comentário (formato filtrado - 4 campos):")
    print(f"  Arquivo: {specific_comments[0].get('file_path')}")
    print(f"  Comentário: {specific_comments[0].get('comment_body')[:80]}...")

# Exemplo 2c: Extrair comentários com formato completo
print("\n\n=== Exemplo 2c: Extrair de um PR específico (COMPLETO) ===")
specific_comments_full = extractor.extract_all_bot_comments(specific_pr=specific_pr_number, filtered=False)

if specific_comments_full:
    print(f"\nTotal de comentários (formato completo): {len(specific_comments_full)}")
    print("\nPrimeiro comentário (formato completo - 16 campos):")
    first = specific_comments_full[0]
    print(f"  PR: #{first.get('pr_number')} - {first.get('pr_title')}")
    print(f"  Arquivo: {first.get('file_path')}")
    print(f"  Linha: {first.get('line')}")
    print(f"  Comentário: {first.get('comment_body')[:60]}...")
    print(f"  URL: {first.get('comment_url')}")

# Exemplo 3: Salvar em JSON
print("\n\n=== Exemplo 3: Salvar em JSON ===")
if all_comments:
    # Formato filtrado (apenas 4 campos)
    extractor.save_to_json(all_comments, "exemplo_filtrado.json", filtered=True)
    print("✓ Arquivo exemplo_filtrado.json criado (4 campos)")
    
    # Formato completo (todos os campos)
    extractor.save_to_json(all_comments, "exemplo_completo.json", filtered=False)
    print("✓ Arquivo exemplo_completo.json criado (16 campos)")
else:
    print("Nenhum comentário encontrado para salvar.")

# Exemplo 4: Buscar PRs abertos apenas
print("\n\n=== Exemplo 4: Listar PRs abertos ===")
open_prs = extractor.get_pull_requests(state="open", per_page=10)
print(f"PRs abertos: {len(open_prs)}")
for pr in open_prs[:3]:  # Mostra apenas os 3 primeiros
    print(f"  - PR #{pr['number']}: {pr['title']}")
