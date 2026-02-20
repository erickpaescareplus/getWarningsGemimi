@echo off
echo ================================================
echo   INSTALADOR - Extrator de Comentarios do Bot
echo ================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.7 ou superior.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.

REM Instala dependências
echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo [OK] Dependencias instaladas com sucesso!
echo.

REM Cria arquivo .env se não existir
if not exist .env (
    echo Criando arquivo .env...
    copy .env.example .env
    echo.
    echo [IMPORTANTE] Configure o arquivo .env com suas credenciais:
    echo   - GITHUB_TOKEN
    echo   - GITHUB_OWNER
    echo   - GITHUB_REPO
    echo.
    echo Abra o arquivo .env em um editor de texto e preencha os dados.
) else (
    echo [OK] Arquivo .env ja existe.
)

echo.
echo ================================================
echo   INSTALACAO CONCLUIDA!
echo ================================================
echo.
echo Proximos passos:
echo   1. Configure o arquivo .env com suas credenciais
echo   2. Execute: python github_pr_comments_extractor.py
echo.
pause
