@echo off
echo ===========================================
echo   COMPILANDO ORGANIGRAMA ARAGON (CON ICONO)
echo ===========================================
echo Generando ejecutable con identidad visual...

:: Limpiar carpetas de compilaciones anteriores para evitar conflictos
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: 1. Activar el entorno virtual limpio
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
) else if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo [ERROR] No se ha encontrado la carpeta del entorno virtual.
    pause
    exit /b
)

:: 2. Ejecutar PyInstaller con icono y exclusiones de módulos no utilizados
:: --icon: establece el icono del archivo .exe
:: --add-data: incluye el PNG necesario para el icono de la ventana al ejecutar
pyinstaller --noconfirm --onedir --windowed --clean ^
    --name "OrganigramaAragon" ^
    --icon "assets\genfavicon-package\favicon.ico" ^
    --add-data "assets\genfavicon-package\genfavicon-256.png;assets/genfavicon-package" ^
    --hidden-import siu2dict_openpyxl ^
    --exclude-module PySide6.QtWebEngineCore ^
    --exclude-module PySide6.QtWebEngineWidgets ^
    --exclude-module PySide6.Qt3D ^
    --exclude-module PySide6.QtQml ^
    --exclude-module PySide6.QtQuick ^
    --exclude-module PySide6.QtQuickWidgets ^
    --exclude-module PySide6.QtSql ^
    --exclude-module PySide6.QtMultimedia ^
    --exclude-module PySide6.QtBluetooth ^
    --exclude-module PySide6.QtPositioning ^
    --exclude-module PySide6.QtSensors ^
    --exclude-module PySide6.QtTest ^
    "main.py"

echo.
echo ===========================================
echo   PROCESO TERMINADO - VERIFICA LA CARPETA 'dist'
echo   EL ejecutable ya tiene el icono de Aragón.
echo ===========================================
pause
