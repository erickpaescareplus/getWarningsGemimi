"""
Automação para extrair comentários do bot pr-validation-gemini-2 do GitHub
"""
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class GitHubPRCommentsExtractor:
    """Classe para extrair comentários de Pull Requests do GitHub"""
    
    def __init__(self, token: str, owner: str, repo: str, bot_username: str = None, verify_ssl: bool = True):
        """
        Inicializa o extrator de comentários
        
        Args:
            token: Token de acesso do GitHub (fine-grained ou classic)
            owner: Dono do repositório
            repo: Nome do repositório
            bot_username: Nome do bot (opcional, padrão busca por 'pr-validation-gemin' para pegar todas variações)
            verify_ssl: Verificar certificado SSL (False em ambientes corporativos com proxy)
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        # Usa padrão amplo se não especificado (pega gemini-2, gemini, gemimi, etc.)
        self.bot_username = bot_username if bot_username else "pr-validation-gemin"
        self.verify_ssl = verify_ssl
        
        # Suprime aviso de SSL se desabilitado
        if not verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def get_pull_requests(self, state: str = "all", per_page: int = 100) -> List[Dict]:
        """
        Busca todos os Pull Requests do repositório
        
        Args:
            state: Estado dos PRs (open, closed, all)
            per_page: Número de resultados por página
            
        Returns:
            Lista de Pull Requests
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls"
        params = {"state": state, "per_page": per_page}
        
        all_prs = []
        page = 1
        
        while True:
            params["page"] = page
            response = requests.get(url, headers=self.headers, params=params, verify=self.verify_ssl)
            
            if response.status_code != 200:
                print(f"Erro ao buscar PRs: {response.status_code}")
                print(response.json())
                break
            
            prs = response.json()
            if not prs:
                break
            
            all_prs.extend(prs)
            page += 1
            
            # Se retornou menos que per_page, é a última página
            if len(prs) < per_page:
                break
        
        return all_prs
    
    def get_pr_review_comments(self, pr_number: int) -> List[Dict]:
        """
        Busca comentários de revisão de um Pull Request específico
        
        Args:
            pr_number: Número do Pull Request
            
        Returns:
            Lista de comentários de revisão
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/comments"
        params = {"per_page": 100}
        
        all_comments = []
        page = 1
        
        while True:
            params["page"] = page
            response = requests.get(url, headers=self.headers, params=params, verify=self.verify_ssl)
            
            if response.status_code != 200:
                print(f"Erro ao buscar comentários do PR #{pr_number}: {response.status_code}")
                break
            
            comments = response.json()
            if not comments:
                break
            
            all_comments.extend(comments)
            page += 1
            
            if len(comments) < 100:
                break
        
        return all_comments
    
    def filter_bot_comments(self, comments: List[Dict]) -> List[Dict]:
        """
        Filtra comentários do bot de validação (pr-validation-gemini-2, pr-validation-gemimi, etc.)
        
        Args:
            comments: Lista de todos os comentários
            
        Returns:
            Lista de comentários apenas do bot
        """
        bot_comments = []
        
        for comment in comments:
            user = comment.get("user", {})
            username = user.get("login", "")
            
            # Busca ampla: verifica se o username contém o padrão do bot
            if self.bot_username.lower() in username.lower():
                bot_comments.append(comment)
        
        return bot_comments
    
    def extract_comment_data(self, comment: Dict, pr_info: Dict) -> Dict:
        """
        Extrai dados relevantes de um comentário
        
        Args:
            comment: Dados do comentário
            pr_info: Informações do Pull Request
            
        Returns:
            Dicionário com dados formatados
        """
        return {
            "pr_number": pr_info.get("number"),
            "pr_title": pr_info.get("title"),
            "pr_url": pr_info.get("html_url"),
            "pr_state": pr_info.get("state"),
            "file_path": comment.get("path"),
            "line": comment.get("line"),
            "original_line": comment.get("original_line"),
            "diff_hunk": comment.get("diff_hunk"),
            "code_snippet": self.extract_code_from_diff(comment.get("diff_hunk", "")),
            "comment_body": comment.get("body"),
            "comment_created_at": comment.get("created_at"),
            "comment_updated_at": comment.get("updated_at"),
            "comment_url": comment.get("html_url"),
            "commit_id": comment.get("commit_id"),
            "in_reply_to_id": comment.get("in_reply_to_id")
        }
    
    def extract_comment_data_filtered(self, comment: Dict) -> Dict:
        """
        Extrai apenas os dados essenciais de um comentário (versão filtrada)
        
        Args:
            comment: Dados do comentário
            
        Returns:
            Dicionário com apenas as 4 propriedades essenciais
        """
        return {
            "file_path": comment.get("path"),
            "diff_hunk": comment.get("diff_hunk"),
            "code_snippet": self.extract_code_from_diff(comment.get("diff_hunk", "")),
            "comment_body": comment.get("body")
        }
    
    def extract_code_from_diff(self, diff_hunk: str) -> str:
        """
        Extrai o código relevante do diff
        
        Args:
            diff_hunk: Trecho do diff
            
        Returns:
            Código extraído
        """
        if not diff_hunk:
            return ""
        
        lines = diff_hunk.split("\n")
        code_lines = []
        
        for line in lines:
            # Remove linhas de contexto de diff (@@ ...)
            if line.startswith("@@"):
                continue
            # Adiciona linhas de código (removendo +, -, espaço do início)
            if line and len(line) > 1:
                code_lines.append(line[1:])
        
        return "\n".join(code_lines)
    
    def extract_all_bot_comments(self, max_prs: Optional[int] = None, specific_pr: Optional[int] = None, filtered: bool = True) -> List[Dict]:
        """
        Extrai todos os comentários do bot de todos os Pull Requests
        
        Args:
            max_prs: Número máximo de PRs a processar (None para todos)
            specific_pr: Número de um PR específico para processar (None para todos)
            filtered: Se True, retorna apenas 4 campos essenciais; se False, retorna todos os campos
            
        Returns:
            Lista de comentários formatados
        """
        all_bot_comments = []
        
        # Se foi especificado um PR específico
        if specific_pr:
            print(f"Buscando Pull Request #{specific_pr}...")
            url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{specific_pr}"
            response = requests.get(url, headers=self.headers, verify=self.verify_ssl)
            
            if response.status_code != 200:
                print(f"❌ Erro ao buscar PR #{specific_pr}: {response.status_code}")
                if response.status_code == 404:
                    print(f"   PR #{specific_pr} não encontrado no repositório {self.owner}/{self.repo}")
                return []
            
            pr = response.json()
            prs = [pr]
            print(f"✓ PR #{specific_pr} encontrado: {pr.get('title')}")
        else:
            # Busca todos os PRs
            print(f"Buscando Pull Requests do repositório {self.owner}/{self.repo}...")
            prs = self.get_pull_requests()
            
            if max_prs:
                prs = prs[:max_prs]
            
            print(f"Encontrados {len(prs)} Pull Requests. Processando...")
        
        # Processa os PRs
        for i, pr in enumerate(prs, 1):
            pr_number = pr.get("number")
            
            if specific_pr:
                print(f"\nProcessando PR #{pr_number}: {pr.get('title')}")
            else:
                print(f"[{i}/{len(prs)}] Processando PR #{pr_number}: {pr.get('title')}")
            
            # Busca comentários do PR
            comments = self.get_pr_review_comments(pr_number)
            
            # Filtra apenas comentários do bot
            bot_comments = self.filter_bot_comments(comments)
            
            if bot_comments:
                print(f"  ✓ Encontrados {len(bot_comments)} comentários do bot")
                
                # Extrai dados relevantes
                for comment in bot_comments:
                    if filtered:
                        comment_data = self.extract_comment_data_filtered(comment)
                    else:
                        comment_data = self.extract_comment_data(comment, pr)
                    all_bot_comments.append(comment_data)
            else:
                print("  - Nenhum comentário do bot encontrado")
        
        return all_bot_comments
    
    def save_to_json(self, data: List[Dict], output_file: str = "bot_comments.json", filtered: bool = True):
        """
        Salva os dados em um arquivo JSON
        
        Args:
            data: Dados a serem salvos
            output_file: Nome do arquivo de saída
            filtered: Se os dados estão filtrados (apenas 4 campos)
        """
        # Se for um arquivo de PR específico, salva na pasta comments-gemimi
        if "PR" in output_file:
            output_dir = "comments-gemimi"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_file)
        else:
            output_path = output_file
        
        if filtered:
            # Formato simplificado (apenas comentários)
            output_data = {
                "metadata": {
                    "repository": f"{self.owner}/{self.repo}",
                    "bot_username": self.bot_username,
                    "total_comments": len(data),
                    "extracted_at": datetime.now().isoformat(),
                    "format": "filtered"
                },
                "comments": data
            }
        else:
            # Formato completo (com todos os dados)
            output_data = {
                "metadata": {
                    "repository": f"{self.owner}/{self.repo}",
                    "bot_username": self.bot_username,
                    "total_comments": len(data),
                    "extracted_at": datetime.now().isoformat(),
                    "format": "complete"
                },
                "comments": data
            }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Dados salvos em: {output_path}")
        print(f"✓ Total de comentários extraídos: {len(data)}")


def main():
    """Função principal"""
    
    # Carrega configurações das variáveis de ambiente
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER")  # Ex: "microsoft"
    GITHUB_REPO = os.getenv("GITHUB_REPO")    # Ex: "vscode"
    BOT_USERNAME = os.getenv("BOT_USERNAME")  # Opcional: nome do bot (padrão busca por 'pr-validation-gemin')
    
    # Opção para desabilitar verificação SSL (ambientes corporativos com proxy)
    DISABLE_SSL_VERIFY = os.getenv("DISABLE_SSL_VERIFY", "false").lower() == "true"
    
    # Validação
    if not GITHUB_TOKEN:
        print("❌ ERRO: Variável de ambiente GITHUB_TOKEN não definida")
        print("   Configure o token no arquivo .env ou exporte a variável")
        return
    
    if not GITHUB_OWNER:
        print("❌ ERRO: Variável de ambiente GITHUB_OWNER não definida")
        print("   Configure o dono do repositório no arquivo .env")
        return
    
    if not GITHUB_REPO:
        print("❌ ERRO: Variável de ambiente GITHUB_REPO não definida")
        print("   Configure o nome do repositório no arquivo .env")
        return
    
    # Inicializa o extrator
    extractor = GitHubPRCommentsExtractor(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=GITHUB_REPO,
        bot_username=BOT_USERNAME,
        verify_ssl=not DISABLE_SSL_VERIFY
    )
    
    # Extrai comentários
    print("="*60)
    print("EXTRATOR DE COMENTÁRIOS DO BOT DE VALIDAÇÃO")
    print("="*60)
    print(f"🤖 Bot: {extractor.bot_username}*")
    if DISABLE_SSL_VERIFY:
        print("⚠️ Verificação SSL desabilitada")
    print()
    
    # Solicita o número do PR
    while True:
        pr_input = input("Digite o número do Pull Request: ").strip()
        try:
            specific_pr = int(pr_input)
            if specific_pr <= 0:
                print("❌ Número inválido! Digite um número positivo.")
                continue
            break
        except ValueError:
            print("❌ Entrada inválida! Digite apenas números.")
    
    print()
    
    # Extrai comentários do PR específico
    comments = extractor.extract_all_bot_comments(specific_pr=specific_pr, filtered=True)
    
    # Salva em JSON
    output_file = f"bot_comments_PR{specific_pr}.json"
    extractor.save_to_json(comments, output_file, filtered=True)
    
    print("\n" + "="*60)
    print("EXTRAÇÃO CONCLUÍDA")
    print("="*60)


if __name__ == "__main__":
    main()
