#!/bin/bash

# Script para ejecutar el Dashboard Dorada Control

echo "🚀 Iniciando Dashboard Dorada Control..."
echo "========================================"

# Check if required files exist
if [ ! -f "dashboard.py" ]; then
    echo "❌ Error: dashboard.py no encontrado"
    exit 1
fi

if [ ! -f "config.py" ]; then
    echo "⚠️  Advertencia: config.py no encontrado"
    echo "Copiando config_example.py como config.py..."
    cp config_example.py config.py
    echo "✅ Por favor edita config.py con tus credenciales de base de datos"
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit no está instalado"
    echo "Instalando dependencias..."
    pip3 install -r requirements.txt
fi

# Run the dashboard
echo "🌐 Iniciando dashboard..."
echo "El dashboard estará disponible en: http://localhost:8501"
echo "Presiona Ctrl+C para detener"
echo ""

streamlit run dashboard.py 