#!/bin/bash

# Dorada Dashboard Installation Script

echo "🚀 Instalando Dashboard Dorada Control..."
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8+"
    exit 1
fi

echo "✅ Python 3 encontrado"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Por favor instala pip"
    exit 1
fi

echo "✅ pip3 encontrado"

# Install Python dependencies
echo "📦 Instalando dependencias de Python..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi

# Check if PostgreSQL is running
echo "🔍 Verificando PostgreSQL..."
if ! pg_isready -q; then
    echo "⚠️  PostgreSQL no está ejecutándose o no está instalado"
    echo "Por favor:"
    echo "1. Instala PostgreSQL"
    echo "2. Inicia el servicio PostgreSQL"
    echo "3. Crea la base de datos 'dorada_dashboard'"
    echo "4. Ejecuta: python3 setup_database.py"
else
    echo "✅ PostgreSQL está ejecutándose"
    
    # Setup database
    echo "🗄️  Configurando base de datos..."
    python3 setup_database.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Base de datos configurada"
        
        # Process data
        echo "📊 Procesando datos Excel..."
        python3 data_processor.py
        
        if [ $? -eq 0 ]; then
            echo "✅ Datos procesados correctamente"
            echo ""
            echo "🎉 ¡Instalación completada!"
            echo ""
            echo "Para ejecutar el dashboard:"
            echo "streamlit run dashboard.py"
            echo ""
            echo "El dashboard estará disponible en: http://localhost:8501"
        else
            echo "❌ Error procesando datos"
            exit 1
        fi
    else
        echo "❌ Error configurando base de datos"
        exit 1
    fi
fi 