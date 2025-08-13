#!/usr/bin/env python3
"""
Script to setup PostgreSQL database for Dorada Dashboard
"""

import sys
import logging
from database import DatabaseManager
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_database():
    """Setup the database and create tables"""
    
    logger.info("Iniciando configuración de la base de datos...")
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    # Connect to database
    logger.info("Conectando a PostgreSQL...")
    if not db_manager.connect():
        logger.error("❌ No se pudo conectar a la base de datos")
        logger.error("Verifica que:")
        logger.error("1. PostgreSQL esté ejecutándose")
        logger.error("2. Las credenciales en config.py sean correctas")
        logger.error("3. La base de datos 'dorada_dashboard' exista")
        return False
    
    # Drop existing tables and recreate them
    logger.info("Eliminando tablas existentes...")
    try:
        db_manager.connection.execute(text("DROP TABLE IF EXISTS cumplimiento_plan_desarrollo CASCADE"))
        db_manager.connection.execute(text("DROP TABLE IF EXISTS reporte_financiero CASCADE"))
        db_manager.connection.commit()
        logger.info("✅ Tablas existentes eliminadas")
    except Exception as e:
        logger.error(f"Error eliminando tablas: {e}")
        return False
    
    # Create tables
    logger.info("Creando tablas...")
    try:
        db_manager.create_tables()
        logger.info("✅ Tablas creadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")
        return False
    
    # Close connection
    db_manager.close()
    
    logger.info("✅ Configuración de base de datos completada")
    return True

def main():
    """Main function"""
    print("=" * 50)
    print("🔧 Configuración de Base de Datos - Dorada Dashboard")
    print("=" * 50)
    
    success = setup_database()
    
    if success:
        print("\n✅ Base de datos configurada correctamente")
        print("\n📋 Próximos pasos:")
        print("1. Ejecutar: python data_processor.py")
        print("2. Ejecutar: streamlit run dashboard.py")
    else:
        print("\n❌ Error en la configuración de la base de datos")
        sys.exit(1)

if __name__ == "__main__":
    main() 