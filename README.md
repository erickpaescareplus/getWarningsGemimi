# Automações de Code Review - GitHub & SonarQube

Ferramentas de automação para extrair comentários de bots e alertas de qualidade de código.

## Módulos

1. **GitHub PR Comments** - Extrai comentários do bot pr-validation-gemini
2. **SonarQube Issues** - Extrai alertas e issues do SonarQube ([Documentação](getWarningsSonar/README.md))

---

## GitHub - Extrator de Comentários do Bot

### Configuração

1. Configure o arquivo `.env`:
```env
GITHUB_TOKEN=seu_token_aqui
GITHUB_OWNER=CareplusBR
GITHUB_REPO=nome-do-repositorio
DISABLE_SSL_VERIFY=false
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Uso

```bash
# Extrair comentários de um PR específico
python extrair_pr_especifico.py 102

# Modo interativo
python extrair_pr_especifico.py

# Atalho Windows
extrair_pr.bat 102
```

Resultado: `comments-gemimi/bot_comments_PR{numero}.json`

### Formato do JSON

```json
{
  "metadata": {
    "repository": "CareplusBR/projeto",
    "pull_request": 102,
    "total_comments": 15,
    "extracted_at": "2026-02-20T14:00:00",
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

### Obtendo o Token do GitHub

1. Acesse: https://github.com/settings/tokens/new
2. Marque o escopo: **repo** (Full control)
3. Clique em "Generate token"
4. Copie e cole no arquivo `.env`

---

## SonarQube - Extrator de Issues

Para extrair alertas do SonarQube, acesse a documentação completa:

📁 [getWarningsSonar/README.md](getWarningsSonar/README.md)

---

## Estrutura do Projeto

```
automacaoGemimiValidator/
├── comments-gemimi/              # JSONs dos comentários do GitHub
├── getWarningsSonar/             # Módulo SonarQube
│   ├── sonar-issues/             # JSONs dos alertas do Sonar
│   ├── extrair_sonar_pr.py       # Script principal
│   └── README.md                 # Documentação completa
├── extrair_pr_especifico.py      # Script para extrair comentários do GitHub
├── github_pr_comments_extractor.py  # Classe extratora
├── extrair_pr.bat                # Atalho Windows (GitHub)
├── instalar.bat                  # Instalador de dependências
├── .env                          # Credenciais (não commitar!)
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo
```

## Troubleshooting

| Erro | Solução |
|------|---------|
| `GITHUB_TOKEN não definida` | Configure o `.env` |
| `401 Unauthorized` | Token inválido - gere um novo |
| `404 Not Found` | Verifique GITHUB_OWNER e GITHUB_REPO |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Configure `DISABLE_SSL_VERIFY=true` |
