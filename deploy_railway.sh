#!/bin/bash

# Script de despliegue automatizado para Railway
echo "🚀 Desplegando Dashboard Dorada Control en Railway..."

# Verificar que Railway CLI esté instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no está instalado. Instalando..."
    npm install -g @railway/cli
fi

# Verificar que estemos en el directorio correcto
if [ ! -f "dashboard.py" ]; then
    echo "❌ No se encontró dashboard.py. Asegúrate de estar en el directorio correcto."
    exit 1
fi

# Verificar que los archivos de configuración existan
echo "📋 Verificando archivos de configuración..."
required_files=("requirements.txt" "nixpacks.toml" "railway.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ No se encontró $file"
        exit 1
    fi
done

echo "✅ Archivos de configuración verificados"

# Configurar variables de entorno en Railway
echo "🔧 Configurando variables de entorno..."
railway variables set DB_HOST=yamabiko.proxy.rlwy.net
railway variables set DB_PORT=55829
railway variables set DB_NAME=railway
railway variables set DB_USER=postgres
railway variables set DB_PASSWORD=WlLKHQUeoxDLXqobPEJZCDRbYtzsiVGH

echo "✅ Variables de entorno configuradas"

# Desplegar la aplicación
echo "🚀 Iniciando despliegue..."
railway up

echo "✅ Despliegue completado!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Verificar el estado del despliegue en Railway Dashboard"
echo "2. Configurar el dominio personalizado si es necesario"
echo "3. Monitorear los logs para verificar que todo funcione correctamente"
echo ""
echo "🌐 La aplicación estará disponible en la URL proporcionada por Railway" 