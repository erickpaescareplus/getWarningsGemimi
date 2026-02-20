@echo off
echo ================================================
echo   Teste de Configuracao
echo ================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    exit /b 1
)

REM Verifica se o .env existe
if not exist .env (
    echo [AVISO] Arquivo .env nao encontrado!
    echo.
    echo Execute primeiro: instalar.bat
    echo.
    pause
    exit /b 1
)

REM Executa o script de teste
python testar_configuracao.py

echo.
pause
