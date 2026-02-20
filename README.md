# Automação de Extração de Comentários do Bot PR-Validation-Gemini-2

Este projeto extrai automaticamente todos os comentários feitos pelo bot **pr-validation-gemini-2** em Pull Requests do GitHub e exporta para um arquivo JSON estruturado.

## 📋 Funcionalidades

- ✅ Busca todos os Pull Requests de um repositório
- ✅ Extrai comentários de revisão de código feitos pelo bot
- ✅ Captura informações detalhadas:
  - Código comentado
  - Linha específica do arquivo
  - Sugestão do bot
  - Arquivo e caminho
  - Dados do Pull Request
  - Timestamp dos comentários
- ✅ Exporta tudo em formato JSON estruturado
- ✅ Suporta tokens Fine-grained e Classic do GitHub

## 🔧 Pré-requisitos

- Python 3.7 ou superior
- Conta no GitHub com acesso ao repositório
- Token de acesso do GitHub (Personal Access Token)

## 📦 Instalação

1. **Clone ou baixe este projeto**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure o arquivo `.env`:**
```bash
# Copie o arquivo de exemplo
copy .env.example .env
```

4. **Edite o arquivo `.env` com suas informações:**
```env
GITHUB_TOKEN=seu_token_aqui
GITHUB_OWNER=nome_do_dono_do_repositorio
GITHUB_REPO=nome_do_repositorio
```

## 🔑 Como Criar o Token do GitHub

### Opção 1: Fine-grained Token (Recomendado - Mais Seguro)

1. Acesse: https://github.com/settings/personal-access-tokens/new
2. Configurações necessárias:
   - **Token name**: Nome descritivo (ex: "Bot Comments Extractor")
   - **Expiration**: Escolha a validade do token
   - **Repository access**: Selecione o repositório específico
   - **Permissions** → **Repository permissions**:
     - `Pull requests`: **Read-only** ✅
3. Clique em **Generate token**
4. **Copie o token** (você não poderá vê-lo novamente!)

### Opção 2: Classic Token

1. Acesse: https://github.com/settings/tokens/new
2. Configurações necessárias:
   - **Note**: Nome descritivo
   - **Expiration**: Escolha a validade
   - **Select scopes**:
     - ✅ `public_repo` (para repositórios públicos)
     - ✅ `repo` (para repositórios privados - full control)
3. Clique em **Generate token**
4. **Copie o token**

## ▶️ Como Usar

1. **Execute o script:**
```bash
python github_pr_comments_extractor.py
```

2. **Escolha o modo de extração:**

O script perguntará o que você deseja fazer:

```
Opções de extração:
  1 - Extrair de um PR específico
  2 - Extrair de todos os PRs

Digite sua escolha (1 ou 2):
```

### Opção 1: PR Específico

- Digite `1` e pressione Enter
- Digite o número do Pull Request (ex: `123`)
- O script processará apenas aquele PR
- Arquivo salvo como: `comments-gemimi/bot_comments_PR123.json` ✨
- **Formato**: Apenas 4 campos essenciais (filtrado)

💡 **Use esta opção quando**: Você quer analisar um PR específico rapidamente.

### Opção 2: Todos os PRs

- Digite `2` e pressione Enter
- O script buscará e processará todos os Pull Requests
- **Formato**: Completo com todos os campos
- Arquivo salvo como: `bot_comments.json`

💡 **Use esta opção quando**: Você quer uma análise completa do repositório.

3. **Acompanhe o progresso no console:**
```
===========================================================
EXTRATOR DE COMENTÁRIOS DO BOT PR-VALIDATION-GEMINI-2
===========================================================
Buscando Pull Requests do repositório owner/repo...
Encontrados 50 Pull Requests. Processando...
[1/50] Processando PR #123: Feature XYZ
  ✓ Encontrados 5 comentários do bot
[2/50] Processando PR #122: Fix bug ABC
  - Nenhum comentário do bot encontrado
...
```

## 📄 Formato do JSON de Saída

### Formato Filtrado (Padrão para PRs específicos)

Os arquivos salvos na pasta `comments-gemimi/` contêm apenas os 4 campos essenciais:

```json
{
  "metadata": {
    "repository": "owner/repo",
    "bot_username": "pr-validation-gemini-2",
    "total_comments": 20,
    "extracted_at": "2026-02-20T10:30:00",
    "format": "filtered"
  },
  "comments": [
    {
      "file_path": "src/main.py",
      "diff_hunk": "@@ -42,6 +42,7 @@...",
      "code_snippet": "def funcao():\n    return valor",
      "comment_body": "Sugestão: Adicionar validação de tipo aqui..."
    }
  ]
}
```

### Formato Completo (Todos os PRs)

O arquivo `bot_comments.json` terá a seguinte estrutura completa:

```json
{
  "metadata": {
    "repository": "owner/repo",
    "bot_username": "pr-validation-gemini-2",
    "total_comments": 150,
    "extracted_at": "2026-02-20T10:30:00",
    "format": "complete"
  },
  "comments": [
    {
      "pr_number": 123,
      "pr_title": "Feature: Adiciona nova funcionalidade",
      "pr_url": "https://github.com/owner/repo/pull/123",
      "pr_state": "open",
      "file_path": "src/main.py",
      "line": 45,
      "original_line": 45,
      "diff_hunk": "@@ -42,6 +42,7 @@...",
      "code_snippet": "def funcao():\n    return valor",
      "comment_body": "Sugestão: Adicionar validação de tipo aqui...",
      "comment_created_at": "2026-02-20T09:15:30Z",
      "comment_updated_at": "2026-02-20T09:15:30Z",
      "comment_url": "https://github.com/owner/repo/pull/123#discussion_r123456",
      "commit_id": "abc123def456",
      "in_reply_to_id": null
    }
  ]
}
```

### Campos do Formato Filtrado (4 essenciais):

- **file_path**: Caminho do arquivo comentado
- **diff_hunk**: Contexto do diff (mostra mudanças)
- **code_snippet**: Código extraído do diff
- **comment_body**: Texto completo do comentário/sugestão do bot

- **pr_number**: Número do Pull Request
- **pr_title**: Título do PR
- **pr_url**: Link para o PR
- **pr_state**: Estado (open, closed, merged)
- **file_path**: Caminho do arquivo comentado
- **line**: Linha atual do código comentada
- **original_line**: Linha original no diff
- **diff_hunk**: Contexto do diff (mostra mudanças)
- **code_snippet**: Código extraído do diff
- **comment_body**: Texto completo do comentário/sugestão do bot
- **comment_created_at**: Data de criação do comentário
- **comment_updated_at**: Data de última atualização
- **comment_url**: Link direto para o comentário
- **commit_id**: ID do commit comentado
- **in_reply_to_id**: ID se for resposta a outro comentário

## ⚙️ Personalização

### Limitar Número de PRs (Para Testes)

Edite o arquivo `github_pr_comments_extractor.py` na função `main()`:

```python
# Processar apenas os 10 PRs mais recentes
comments = extractor.extract_all_bot_comments(max_prs=10)
```

### Mudar Nome do Bot

Se o bot tiver um nome ligeiramente diferente, edite a classe:

```python
self.bot_username = "pr-validation-gemini-2"  # Altere aqui
```

### Alterar Nome do Arquivo de Saída

```python
output_file = "meus_comentarios.json"  # Altere aqui
extractor.save_to_json(comments, output_file)
```

## 🐛 Troubleshooting

### Erro: "GITHUB_TOKEN não definida"
- Certifique-se de ter criado o arquivo `.env`
- Verifique se o token está corretamente configurado no `.env`

### Erro 401 (Unauthorized)
- Token inválido ou expirado
- Gere um novo token no GitHub

### Erro 403 (Forbidden)
- Token sem permissões necessárias
- Adicione permissão de leitura em Pull Requests

### Erro 404 (Not Found)
- Repositório não existe ou token não tem acesso
- Verifique `GITHUB_OWNER` e `GITHUB_REPO` no `.env`

### Nenhum comentário encontrado
- Verifique se o bot realmente comentou nos PRs
- Confirme se o nome do bot está correto
- O bot pode ter um username diferente (ex: `pr-validation-gemini-2[bot]`)

## 📊 Exemplos de Uso

### Analisar apenas PRs abertos

Modifique o método na classe:

```python
prs = self.get_pull_requests(state="open")  # Apenas abertos
```

### Filtrar por data

Adicione filtro após extrair comentários:

```python
from datetime import datetime, timedelta

# Apenas comentários dos últimos 30 dias
data_limite = datetime.now() - timedelta(days=30)
comentarios_recentes = [
    c for c in comments 
    if datetime.fromisoformat(c['comment_created_at'].replace('Z', '+00:00')) > data_limite
]
```

## 📝 Licença

Este projeto é de código aberto e pode ser usado livremente.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Desenvolvido para automatizar a extração de comentários do bot pr-validation-gemini-2** 🤖
