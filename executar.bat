@echo off
echo ================================================
echo   Executando Extrator de Comentarios do Bot
echo ================================================
echo.

REM Verifica se o .env existe
if not exist .env (
    echo [ERRO] Arquivo .env nao encontrado!
    echo.
    echo Execute primeiro: instalar.bat
    echo E configure o arquivo .env com suas credenciais.
    echo.
    pause
    exit /b 1
)

REM Executa o script
python github_pr_comments_extractor.py

echo.
echo ================================================
echo   Execucao finalizada!
echo ================================================
echo.
pause
