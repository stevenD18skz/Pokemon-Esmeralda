#!/bin/bash

# Instala los paquetes listados en requirements.txt usando pip

if [ ! -f requirements.txt ]; then
    echo "No se encontró el archivo requirements.txt"
    exit 1
fi

# Verifica si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "pip no está instalado. Instalando pip..."
    python -m ensurepip --upgrade
fi

echo "Instalando dependencias de requirements.txt..."
pip install -r requirements.txt

echo "Instalación completada."./ola.bash
