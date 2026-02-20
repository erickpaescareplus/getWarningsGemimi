# 🤖 Extrator de Comentários do Bot PR-Validation-Gemini-2

Automação em Python que extrai comentários do bot **pr-validation-gemini-2** de Pull Requests do GitHub e exporta para JSON.

## 🚀 Instalação Rápida

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar credenciais
copy .env.example .env
# Edite o .env com suas informações
```

## ⚙️ Configuração do .env

```env
# Token do GitHub (https://github.com/settings/tokens)
GITHUB_TOKEN=seu_token_aqui

# Informações do repositório
# Exemplo: https://github.com/CareplusBR/meu-repo
GITHUB_OWNER=CareplusBR
GITHUB_REPO=meu-repo

# [Opcional] Desabilitar SSL (apenas em ambientes corporativos com proxy)
DISABLE_SSL_VERIFY=false
```

### 🔑 Como criar o Token

1. Acesse: https://github.com/settings/tokens/new
2. Marque o escopo: **`repo`** (Full control)
3. Gere e copie o token
4. Cole no `.env`

## 📋 Como Usar

### Extrair Comentários de um PR Específico

```bash
# Forma 1: Direto com número do PR
python extrair_pr_especifico.py 102

# Forma 2: Script interativo (solicita o número)
python extrair_pr_especifico.py

# Forma 3: Atalho Windows
extrair_pr.bat 102
```

**Resultado:**
- Arquivo salvo em: `comments-gemimi/bot_comments_PR102.json`
Cada extração gera um arquivo JSON com 4 campos essenciais:

```json
{
  "metadata": {
    "repository": "CareplusBR/meu-repo",
    "total_comments": 20,
    "format": "filtered"
  },
  "comments": [
    {
      "file_path": "src/app/component.ts",
      "diff_hunk": "@@ -48,7 +48,7 @@\n-  old code\n+  new code",
      "code_snippet": "código extraído do diff",
      "comment_body": "Sugestão do bot aqui..."
    }
  ]
}
```

**Campos:**
- `file_path` - Caminho do arquivo comentado
- `diff_hunk` - Diff do Git com contexto
- `code_snippet` - Código limpo extraído
- `comment_body` - Comentário/sugestão do bot

### Todos os PRs (Completo - 16 campos)

Inclui: PR info, timestamps, URLs, linha do código, etc.

##Arquivo | Descrição |
|---------|-----------|
| `extrair_pr_especifico.py` | Script principal - extrai comentários de um PR |
| `extrair_pr.bat` | Atalho Windows para executar o script |
| `instalar.bat` | Instala dependências e configura o projeto
| `extrair_pr_especifico.py` | Extrai PR específico | `python extrair_pr_especifico.py 102` |
| `github_pr_comments_extractor.py` | Script principal interativo | `python github_pr_comments_extractor.py` |

## ❓ Troubleshooting

| Erro | Solução |
|------|---------|
| `GITHUB_TOKEN não definida` | Configure o arquivo `.env` |
| `401 Unauthorized` | Token inválido - gere um novo |
| `403 Forbidden` | Token sem permissão - adicione escopo `repo` |
| `404 Not Found` | Verifique GITHUB_OWNER e GITHUB_REPO |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Configure `DISABLE_SSL_VERIFY=true` no `.env` |
| Nenhum comentário encontrado | Verifique se o bot comentou no PR |

## 📁 Estrutura de Pastas
extraídos dos PRs
│   └── bot_comments_PR{numero}.json
├── extrair_pr_especifico.py  # Script principal
├── github_pr_comments_extractor.py  # Classe do extrator
├── extrair_pr.bat            # Atalho Windows
├── instalar.bat              # Instalador
├── .env                      # Suas credenciais
├── .env.example              # Modelo de configuração
└── requirements.txt          # DependênciasPR
├── .env                     # Suas credenciais (não commitar!)
├── .eExemplo de Uso Completo

```bash
# 1. Instalar (apenas primeira vez)
pip install -r requirements.txt

# 2. Configurar .env
# Edite o arquivo .env com seu token e repositório

# 3. Extrair comentários do PR #102
python extrair_pr_especifico.py 102

# 4. Ver resultado
# Arquivo: comments-gemimi/bot_comments_PR102.json
```
```
✅ Relatório completo  
✅ Histórico com timestamps  
✅ Links para GitHub  

## 📦 Dependências

- `requests` - Chamadas à API do GitHub
- `python-dotenv` - Gerenciamento de variáveis de ambiente
