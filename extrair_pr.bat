@echo off
echo ================================================
echo   Extrator de PR Especifico
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

REM Verifica se passou o número do PR como parâmetro
if "%1"=="" (
    REM Solicita o número do PR
    set /p PR_NUMBER="Digite o numero do Pull Request: "
) else (
    set PR_NUMBER=%1
)

REM Executa o script
python extrair_pr_especifico.py %PR_NUMBER%

echo.
pause
