#!/bin/bash

# Script de configuración para el despliegue
echo "🚀 Configurando Dashboard Dorada Control..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Configurar base de datos
echo "🗄️ Configurando base de datos..."
python setup_database.py

# Procesar datos
echo "📊 Procesando datos..."
python data_processor.py

echo "✅ Configuración completada!"
echo "🌐 Iniciando dashboard..." 