#!/usr/bin/env python3
"""
Script para configurar la base de datos de Railway con los datos del proyecto
"""

import os
import sys
import logging
from sqlalchemy import text
from database import DatabaseManager
from data_processor import process_cumplimiento_data, process_financiero_data

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Railway
RAILWAY_CONFIG = {
    'host': 'yamabiko.proxy.rlwy.net',
    'port': '55829',
    'database': 'railway',
    'user': 'postgres',
    'password': 'WlLKHQUeoxDLXqobPEJZCDRbYtzsiVGH'
}

def setup_railway_database():
    """Configurar la base de datos de Railway"""
    print("🚀 Configurando Base de Datos de Railway...")
    
    try:
        # Crear instancia de DatabaseManager con configuración de Railway
        db_manager = DatabaseManager(
            host=RAILWAY_CONFIG['host'],
            port=RAILWAY_CONFIG['port'],
            database=RAILWAY_CONFIG['database'],
            user=RAILWAY_CONFIG['user'],
            password=RAILWAY_CONFIG['password']
        )
        
        # Conectar a la base de datos
        logger.info("Conectando a Railway PostgreSQL...")
        db_manager.connect()
        
        # Eliminar tablas existentes si existen
        logger.info("Eliminando tablas existentes...")
        db_manager.drop_tables()
        
        # Crear tablas
        logger.info("Creando tablas...")
        db_manager.create_tables()
        
        # Procesar y cargar datos de cumplimiento
        logger.info("Procesando datos de cumplimiento...")
        cumplimiento_data = process_cumplimiento_data()
        
        # Procesar y cargar datos financieros
        logger.info("Procesando datos financieros...")
        financiero_data = process_financiero_data()
        
        # Insertar datos de cumplimiento
        logger.info("Insertando datos de cumplimiento...")
        if isinstance(cumplimiento_data, list):
            # Si es una lista de DataFrames, tomar el primero
            cumplimiento_df = cumplimiento_data[0] if cumplimiento_data else None
        else:
            cumplimiento_df = cumplimiento_data
        
        if cumplimiento_df is not None:
            db_manager.insert_cumplimiento_data(cumplimiento_df)
        
        # Insertar datos financieros
        logger.info("Insertando datos financieros...")
        if isinstance(financiero_data, list):
            # Si es una lista de DataFrames, tomar el primero
            financiero_df = financiero_data[0] if financiero_data else None
        else:
            financiero_df = financiero_data
        
        if financiero_df is not None:
            db_manager.insert_financiero_data(financiero_df)
        
        logger.info("✅ Base de datos de Railway configurada exitosamente!")
        
        # Mostrar estadísticas
        cumplimiento_count = db_manager.get_cumplimiento_count()
        financiero_count = db_manager.get_financiero_count()
        
        print(f"\n📊 Estadísticas de la base de datos:")
        print(f"   • Registros de cumplimiento: {cumplimiento_count}")
        print(f"   • Registros financieros: {financiero_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error configurando la base de datos: {e}")
        return False

def test_connection():
    """Probar la conexión a Railway"""
    print("🔍 Probando conexión a Railway...")
    
    try:
        db_manager = DatabaseManager(
            host=RAILWAY_CONFIG['host'],
            port=RAILWAY_CONFIG['port'],
            database=RAILWAY_CONFIG['database'],
            user=RAILWAY_CONFIG['user'],
            password=RAILWAY_CONFIG['password']
        )
        
        db_manager.connect()
        print("✅ Conexión exitosa a Railway!")
        
        # Probar consulta simple
        result = db_manager.connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"📋 Versión de PostgreSQL: {version[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Configuración de Base de Datos - Railway")
    print("=" * 60)
    
    # Probar conexión primero
    if test_connection():
        # Configurar base de datos
        if setup_railway_database():
            print("\n🎉 ¡Configuración completada exitosamente!")
            print("\n📋 Próximos pasos:")
            print("1. Actualizar config.py con las credenciales de Railway")
            print("2. Ejecutar: streamlit run dashboard.py")
        else:
            print("\n❌ Error en la configuración")
            sys.exit(1)
    else:
        print("\n❌ No se pudo conectar a Railway")
        sys.exit(1) 