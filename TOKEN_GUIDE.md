# 🔐 Guia Completo de Tokens do GitHub

Este guia detalha como criar e configurar tokens de acesso para a API do GitHub.

## 📋 Tipos de Tokens

O GitHub oferece dois tipos de tokens:

### 1. Fine-grained Tokens (Novo - Recomendado)
- ✅ Mais seguro e específico
- ✅ Acesso granular por repositório
- ✅ Permissões específicas
- ❌ Requer mais configuração

### 2. Classic Tokens (Tradicional)
- ✅ Mais simples de configurar
- ✅ Funciona com todos os repositórios
- ❌ Menos seguro (acesso mais amplo)
- ❌ Pode dar mais permissões que o necessário

## 🎯 Qual Token Usar?

| Situação | Token Recomendado |
|----------|-------------------|
| Uso pessoal, 1 repositório | Fine-grained |
| Múltiplos repositórios | Classic |
| Ambiente de produção | Fine-grained |
| Testes rápidos | Classic |

---

## 🔑 Criar Token Fine-grained (Recomendado)

### Passo 1: Acessar Configurações

1. Faça login no GitHub
2. Clique na sua foto (canto superior direito)
3. Vá em **Settings** (Configurações)
4. No menu lateral esquerdo, role até o final
5. Clique em **Developer settings**
6. Clique em **Personal access tokens**
7. Clique em **Fine-grained tokens**
8. Clique no botão **Generate new token**

**Link direto**: https://github.com/settings/personal-access-tokens/new

### Passo 2: Configurar o Token

#### 2.1 Informações Básicas

- **Token name** (Nome do token):
  ```
  Bot Comment Extractor - Automação
  ```
  *(Use um nome descritivo para lembrar depois)*

- **Expiration** (Expiração):
  - Recomendado: `90 dias`
  - Alternativas: 30, 60, 90 dias, ou Custom
  - ⚠️ Após expirar, você precisará gerar um novo

- **Description** (Opcional):
  ```
  Token para extrair comentários do bot pr-validation-gemini-2
  ```

#### 2.2 Acesso ao Repositório

- **Repository access**:
  - Selecione: `Only select repositories` ✅
  - Clique em **Select repositories**
  - Escolha o repositório específico

#### 2.3 Permissões

Em **Repository permissions**, configure:

| Permissão | Nível | Necessário |
|-----------|-------|------------|
| **Pull requests** | **Read-only** | ✅ Obrigatório |
| Contents | Nenhum | ❌ |
| Issues | Nenhum | ❌ |
| Metadata | Read-only | ✅ (Automático) |

⚠️ **Importante**: A permissão `Metadata` será automaticamente selecionada como `Read-only` - isso é normal e necessário.

#### 2.4 Finalizar

1. Revise todas as configurações
2. Clique no botão verde **Generate token**
3. **COPIE O TOKEN IMEDIATAMENTE** ⚠️
   - Formato: `github_pat_XXXXXXXXXXXXX...`
   - Ele só aparece uma vez!
   - Se perder, terá que gerar outro

### Passo 3: Salvar o Token

```env
GITHUB_TOKEN=github_pat_11ABCDEFGH1234567890abcdefghijklmnopqr
```

---

## 🔑 Criar Token Classic

### Passo 1: Acessar Configurações

1. Faça login no GitHub
2. Clique na sua foto (canto superior direito)
3. Vá em **Settings**
4. No menu lateral, role até **Developer settings**
5. Clique em **Personal access tokens**
6. Clique em **Tokens (classic)**
7. Clique no botão **Generate new token (classic)**

**Link direto**: https://github.com/settings/tokens/new

### Passo 2: Configurar o Token

#### 2.1 Informações Básicas

- **Note** (Nome):
  ```
  Bot Comment Extractor
  ```

- **Expiration**:
  - Recomendado: `90 days`

#### 2.2 Selecionar Escopos (Scopes)

Marque **APENAS** o necessário:

**Para repositórios PÚBLICOS:**
- ✅ `public_repo` - Access public repositories

**Para repositórios PRIVADOS (ou públicos e privados):**
- ✅ `repo` - Full control of private repositories
  - ⚠️ Marque APENAS esta opção, ela já inclui automaticamente:
    - `repo:status`
    - `repo_deployment`
    - `public_repo` (acesso a repos públicos também)
    - `repo:invite`
    - `security_events`

**⚠️ NÃO marque outros escopos** (admin:org, delete_repo, etc.) - não são necessários!

**💡 Dica**: Se você trabalha com repositórios privados, marque apenas `repo` - é suficiente para tudo!

#### 2.3 Finalizar

1. Role até o final da página
2. Clique no botão verde **Generate token**
3. **COPIE O TOKEN** ⚠️
   - Formato: `ghp_XXXXXXXXXXXXX...`
   - Só aparece uma vez!

### Passo 3: Salvar o Token

```env
GITHUB_TOKEN=ghp_abc123xyz789defghijklmnopqrstuvwxyz
```

---

## 🔒 Segurança do Token

### ✅ Boas Práticas

1. **Nunca compartilhe seu token**
   - Não poste em GitHub, Discord, Slack, etc.
   - Não envie por email ou mensagem

2. **Use arquivo .env**
   - Token fica local na sua máquina
   - Não é commitado no Git (.gitignore)

3. **Defina expiração**
   - Tokens não devem ser eternos
   - Renove a cada 90 dias

4. **Permissões mínimas**
   - Dê apenas acesso de leitura
   - Apenas ao repositório necessário (fine-grained)

5. **Revogue tokens antigos**
   - Acesse: https://github.com/settings/tokens
   - Delete tokens que não usa mais

### ❌ O Que NÃO Fazer

- ❌ Commitar o token no Git
- ❌ Compartilhar o token com outras pessoas
- ❌ Usar o mesmo token em múltiplas aplicações
- ❌ Dar mais permissões que o necessário
- ❌ Criar tokens sem expiração

---

## 🔍 Verificar e Testar o Token

### Teste 1: Validar Token

Execute este comando no PowerShell:

```powershell
curl -H "Authorization: Bearer SEU_TOKEN_AQUI" https://api.github.com/user
```

**Resposta esperada**: Seus dados do GitHub (username, id, bio, etc.)

### Teste 2: Verificar Acesso ao Repositório

```powershell
curl -H "Authorization: Bearer SEU_TOKEN_AQUI" https://api.github.com/repos/OWNER/REPO
```

Substitua:
- `SEU_TOKEN_AQUI` pelo seu token
- `OWNER` pelo dono do repositório
- `REPO` pelo nome do repositório

**Resposta esperada**: Dados do repositório (name, description, stars, etc.)

### Teste 3: Executar Script de Teste

Crie um arquivo `teste_token.py`:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo = os.getenv("GITHUB_REPO")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# Teste 1: Verificar token
response = requests.get("https://api.github.com/user", headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ Token válido! Logado como: {user['login']}")
else:
    print(f"❌ Token inválido: {response.status_code}")
    exit(1)

# Teste 2: Verificar acesso ao repositório
url = f"https://api.github.com/repos/{owner}/{repo}"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    repo_data = response.json()
    print(f"✅ Acesso ao repositório OK: {repo_data['full_name']}")
else:
    print(f"❌ Sem acesso ao repositório: {response.status_code}")
    exit(1)

# Teste 3: Verificar permissão de Pull Requests
url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
response = requests.get(url, headers=headers, params={"per_page": 1})
if response.status_code == 200:
    print("✅ Permissão de leitura de Pull Requests OK!")
else:
    print(f"❌ Sem permissão para Pull Requests: {response.status_code}")

print("\n🎉 Todos os testes passaram! Pode executar a automação.")
```

Execute:
```bash
python teste_token.py
```

---

## 🔄 Renovar Token Expirado

Quando o token expirar, você verá erro `401 Unauthorized`.

### Opções:

#### 1. Gerar Novo Token
- Volte para as instruções de criação acima
- Gere um novo token
- Substitua no arquivo `.env`

#### 2. Fine-grained: Renovar Token Existente
1. Acesse: https://github.com/settings/personal-access-tokens
2. Clique no token expirado
3. Clique em **Regenerate token**
4. Atualize no `.env`

---

## 📊 Limites da API do GitHub

O GitHub impõe limites de requisições:

| Tipo de Token | Limite por Hora |
|---------------|-----------------|
| Sem autenticação | 60 requisições |
| Com token | 5.000 requisições |

**Para este script**: 
- Cada PR = 1 requisição
- Repositório com 100 PRs = ~100 requisições
- Você pode processar milhares de PRs por hora ✅

---

## ❓ Troubleshooting

### Erro: 401 Unauthorized

**Causas:**
- Token inválido
- Token expirado
- Token não copiado corretamente

**Solução:**
1. Gere um novo token
2. Copie cuidadosamente (sem espaços)
3. Cole no `.env`

### Erro: 403 Forbidden

**Causas:**
- Token sem permissões necessárias
- Limite de API excedido

**Solução:**
1. Verifique permissões do token:
   - Fine-grained: `Pull requests - Read`
   - Classic: `repo` ou `public_repo`
2. Aguarde 1 hora se excedeu o limite

### Erro: 404 Not Found

**Causas:**
- Repositório não existe
- Token sem acesso ao repositório
- Owner ou Repo incorreto no `.env`

**Solução:**
1. Verifique `GITHUB_OWNER` e `GITHUB_REPO`
2. Confirme que o token tem acesso ao repo
3. Para fine-grained: adicione o repo nas configurações

---

## 📞 Links Úteis

- [Gerenciar Tokens Fine-grained](https://github.com/settings/personal-access-tokens)
- [Gerenciar Tokens Classic](https://github.com/settings/tokens)
- [Documentação API GitHub](https://docs.github.com/en/rest)
- [Limites da API](https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api)

---

**Pronto! Seu token está configurado e seguro!** 🔐
