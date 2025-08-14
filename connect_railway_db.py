#!/usr/bin/env python3
"""
Script para conectar el proyecto con la base de datos de Railway
"""

import os
import sys
import logging
from database import DatabaseManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_railway_db_config():
    """Obtener configuración de Railway automáticamente"""
    print("🔍 Detectando configuración de Railway...")
    
    # Railway proporciona estas variables automáticamente
    railway_vars = {
        'PGHOST': os.getenv('PGHOST'),
        'PGPORT': os.getenv('PGPORT'),
        'PGDATABASE': os.getenv('PGDATABASE'),
        'PGUSER': os.getenv('PGUSER'),
        'PGPASSWORD': os.getenv('PGPASSWORD'),
        'DATABASE_URL': os.getenv('DATABASE_URL')
    }
    
    print("📋 Variables de Railway detectadas:")
    for key, value in railway_vars.items():
        if value:
            if 'PASSWORD' in key:
                print(f"   • {key}: {'*' * len(value)}")
            else:
                print(f"   • {key}: {value}")
        else:
            print(f"   • {key}: No disponible")
    
    return railway_vars

def test_railway_connection():
    """Probar conexión a Railway usando variables automáticas"""
    print("\n🔍 Probando conexión a Railway...")
    
    try:
        # Usar configuración automática de Railway
        db_manager = DatabaseManager()
        db_manager.connect()
        
        print("✅ Conexión exitosa a Railway!")
        
        # Probar consulta simple
        from sqlalchemy import text
        result = db_manager.connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"📋 Versión de PostgreSQL: {version[0]}")
        
        # Verificar tablas
        cumplimiento_count = db_manager.get_cumplimiento_count()
        financiero_count = db_manager.get_financiero_count()
        
        print(f"\n📊 Datos en la base de datos:")
        print(f"   • Registros de cumplimiento: {cumplimiento_count}")
        print(f"   • Registros financieros: {financiero_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def setup_railway_connection():
    """Configurar conexión con Railway"""
    print("🚀 Configurando conexión con Railway...")
    
    # Obtener configuración automática
    railway_config = get_railway_db_config()
    
    if not railway_config['PGHOST']:
        print("❌ No se detectaron variables de Railway")
        print("💡 Asegúrate de que el proyecto esté desplegado en Railway")
        return False
    
    # Probar conexión
    if test_railway_connection():
        print("\n🎉 ¡Conexión con Railway configurada exitosamente!")
        print("\n📋 Información de conexión:")
        print(f"   • Host: {railway_config['PGHOST']}")
        print(f"   • Puerto: {railway_config['PGPORT']}")
        print(f"   • Base de datos: {railway_config['PGDATABASE']}")
        print(f"   • Usuario: {railway_config['PGUSER']}")
        
        return True
    else:
        print("\n❌ No se pudo conectar a Railway")
        return False

def create_railway_env_file():
    """Crear archivo .env con variables de Railway (para desarrollo local)"""
    print("\n📝 Creando archivo .env para desarrollo local...")
    
    railway_config = get_railway_db_config()
    
    env_content = f"""# Variables de Railway para desarrollo local
# Copia estas variables desde el dashboard de Railway

DB_HOST={railway_config.get('PGHOST', 'localhost')}
DB_PORT={railway_config.get('PGPORT', '5432')}
DB_NAME={railway_config.get('PGDATABASE', 'railway')}
DB_USER={railway_config.get('PGUSER', 'postgres')}
DB_PASSWORD={railway_config.get('PGPASSWORD', 'your_password_here')}

# URL completa de la base de datos
DATABASE_URL={railway_config.get('DATABASE_URL', '')}
"""
    
    try:
        with open('.env.railway', 'w') as f:
            f.write(env_content)
        print("✅ Archivo .env.railway creado")
        print("💡 Copia las variables desde Railway Dashboard a este archivo")
    except Exception as e:
        print(f"❌ Error creando archivo: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔗 Conexión con Base de Datos Railway")
    print("=" * 60)
    
    if setup_railway_connection():
        print("\n📋 Próximos pasos:")
        print("1. El proyecto ya está conectado a Railway")
        print("2. Ejecutar: streamlit run dashboard.py")
        print("3. El dashboard usará automáticamente la base de datos de Railway")
        
        # Crear archivo .env para referencia
        create_railway_env_file()
    else:
        print("\n❌ Error en la configuración")
        print("\n💡 Soluciones:")
        print("1. Verificar que el proyecto esté desplegado en Railway")
        print("2. Verificar que las variables de entorno estén configuradas")
        print("3. Revisar los logs de Railway")
        sys.exit(1) 