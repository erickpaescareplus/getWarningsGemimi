# 🚀 Guia Rápido de Início

Este guia vai te ajudar a configurar e executar a automação em **5 minutos**.

## ⚡ Instalação Rápida (Windows)

1. **Execute o instalador**:
   ```bash
   instalar.bat
   ```
   Este comando vai:
   - Verificar se Python está instalado
   - Instalar todas as dependências necessárias
   - Criar o arquivo `.env` para você

2. **Configure suas credenciais**:
   - Abra o arquivo `.env` com o Bloco de Notas
   - Preencha os 3 campos:
     ```env
     GITHUB_TOKEN=ghp_SEU_TOKEN_AQUI
     GITHUB_OWNER=nome-do-dono
     GITHUB_REPO=nome-do-repositorio
     ```

3. **Execute a automação**:
   ```bash
   executar.bat
   ```

## 🔑 Como Obter o Token GitHub

### Método 1: Token Fine-grained (Recomendado)

1. **Acesse**: https://github.com/settings/personal-access-tokens/new

2. **Preencha**:
   - **Token name**: `Bot Comment Extractor`
   - **Expiration**: 90 dias (ou o que preferir)
   - **Repository access**: Selecione o repositório específico

3. **Em Permissions → Repository permissions**:
   - Procure `Pull requests`
   - Selecione: **Read-only** (acesso de leitura) ✅

4. **Clique em**: `Generate token`

5. **COPIE O TOKEN** (você só verá uma vez!)

### Método 2: Token Classic (Mais Simples)

1. **Acesse**: https://github.com/settings/tokens/new

2. **Preencha**:
   - **Note**: `Bot Comment Extractor`
   - **Expiration**: 90 dias

3. **Selecione o escopo**:
   - ✅ `public_repo` (para repositórios públicos)
   - ✅ `repo` (para repositórios privados)

4. **Clique em**: `Generate token`

5. **COPIE O TOKEN**

## 📝 Exemplo de Configuração

### Se seu repositório é:
```
https://github.com/facebook/react
```

### Seu .env deve ser:
```env
GITHUB_TOKEN=ghp_abc123xyz789...
GITHUB_OWNER=facebook
GITHUB_REPO=react
```

## ▶️ Executando pela Primeira Vez

### Opção 1: Script Batch (Windows)
```bash
executar.bat
```

### Opção 2: Linha de Comando
```bash
python github_pr_comments_extractor.py
```

### Escolha o que extrair:

O script perguntará:
```
Opções de extração:
  1 - Extrair de um PR específico
  2 - Extrair de todos os PRs

Digite sua escolha (1 ou 2):
```

- **Opção 1**: Digite o número do PR (ex: `123`) - Rápido para análise pontual ⚡
  - Salva em: `comments-gemimi/bot_comments_PR123.json`
  - Formato: **4 campos essenciais** (file_path, diff_hunk, code_snippet, comment_body)
- **Opção 2**: Processa todos os PRs - Análise completa do repositório 📊
  - Salva em: `bot_comments.json`
  - Formato: **Completo** (todos os campos)

## 📊 Resultado

Após a execução, você terá um arquivo JSON com os comentários:

### PR Específico (Formato Filtrado)
- **Local**: `comments-gemimi/bot_comments_PR123.json`
- **Campos**: Apenas os 4 essenciais para revisão de código

```json
{
  "comments": [
    {
      "file_path": "src/main.py",
      "diff_hunk": "@@ ...",
      "code_snippet": "código aqui",
      "comment_body": "Sugestão do bot"
    }
  ]
}
```

### Todos os PRs (Formato Completo)
- **Local**: `bot_comments.json`
- **Campos**: Todos os detalhes (PR info, timestamps, URLs, etc)

```json
{
  "metadata": {
    "repository": "seu-usuario/seu-repo",
    "total_comments": 42,
    "extracted_at": "2026-02-20T10:30:00"
  },
  "comments": [
    {
      "pr_number": 123,
      "file_path": "src/main.py",
      "line": 45,
      "comment_body": "Sugestão do bot...",
      "code_snippet": "código comentado..."
    }
  ]
}
```

## 🎯 Testando com Poucos PRs

Para testar rapidamente, edite o arquivo `github_pr_comments_extractor.py`:

Na função `main()`, linha ~267:
```python
# Antes (processa todos)
comments = extractor.extract_all_bot_comments()

# Depois (processa apenas 5)
comments = extractor.extract_all_bot_comments(max_prs=5)
```

## 🐛 Problemas Comuns

### ❌ "Python não encontrado"
- Instale Python: https://www.python.org/downloads/
- ✅ Marque a opção "Add Python to PATH" durante instalação

### ❌ "GITHUB_TOKEN não definida"
- Verifique se criou o arquivo `.env`
- Confirme que preencheu o token corretamente
- Não adicione aspas ao redor do token

### ❌ Erro 401 - Unauthorized
- Token inválido ou expirado
- Gere um novo token no GitHub

### ❌ Erro 404 - Not Found
- Repositório não existe
- Token não tem acesso ao repositório
- Verifique `GITHUB_OWNER` e `GITHUB_REPO`

### ❌ "Nenhum comentário encontrado"
- Confirme que o bot comentou nos PRs
- O bot pode usar nome diferente (ex: `pr-validation-gemini-2[bot]`)
- Verifique se há PRs com comentários

## 💡 Dicas

1. **Primeiro teste**: Execute com `max_prs=5` para testar rapidamente
2. **Token seguro**: Nunca compartilhe seu token
3. **Backup**: O token expira, guarde-o em local seguro
4. **Performance**: Para repositórios grandes, pode levar alguns minutos

## 📞 Precisa de Ajuda?

1. Verifique o [README.md](README.md) completo
2. Confira o arquivo [TOKEN_GUIDE.md](TOKEN_GUIDE.md) para mais detalhes
3. Execute `exemplo_uso.py` para ver exemplos de uso

---

**Pronto! Em 5 minutos você terá todos os comentários do bot extraídos!** ✅
