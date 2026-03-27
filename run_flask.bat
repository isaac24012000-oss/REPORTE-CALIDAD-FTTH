@echo off
REM Script para ejecutar Flask fácilmente

echo.
echo ====================================================
echo  Dashboard Control de Auditorias - Flask
echo ====================================================
echo.

REM Verificar si virtualenv existe
if not exist .venv (
    echo [ERROR] Entorno virtual no encontrado
    echo Ejecuta primero: install.bat
    pause
    exit /b 1
)

REM Activar virtualenv
call .venv\Scripts\activate.bat

echo [OK] Iniciando aplicación Flask...
echo.
echo Abre tu navegador en: http://localhost:5000
echo Presiona CTRL+C para detener la aplicación
echo.

python app.py

pause
