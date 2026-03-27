@echo off
REM Script de Instalación Rápida para Dashboard

echo.
echo ====================================================
echo  Dashboard Control de Auditorias - Setup
echo ====================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo Descarga Python desde: https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detectado
echo.

REM Crear entorno virtual si no existe
if not exist .venv (
    echo [INFO] Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
) else (
    echo [OK] Entorno virtual ya existe
)

echo.
echo [INFO] Activando entorno virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual activado

echo.
echo [INFO] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Error durante la instalación de dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas

echo.
echo ====================================================
echo  Instalación completada exitosamente!
echo ====================================================
echo.
echo Para iniciar el dashboard, ejecuta uno de los siguientes comandos:
echo.
echo  [1] Streamlit (Recomendado):
echo     streamlit run streamlit_app.py
echo.
echo  [2] Flask:
echo     python app.py
echo.
echo Luego abre tu navegador en:
echo  - Streamlit: http://localhost:8501
echo  - Flask: http://localhost:5000
echo.
pause
