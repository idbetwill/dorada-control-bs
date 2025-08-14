#!/usr/bin/env python3
"""
Script para verificar los datos en la base de datos de Railway
"""

import logging
from database import DatabaseManager
from config import DB_CONFIG

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_railway_data():
    """Verificar los datos en Railway"""
    print("🔍 Verificando datos en Railway...")
    
    try:
        # Crear instancia de DatabaseManager
        db_manager = DatabaseManager(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        # Conectar a la base de datos
        db_manager.connect()
        
        # Obtener estadísticas
        cumplimiento_count = db_manager.get_cumplimiento_count()
        financiero_count = db_manager.get_financiero_count()
        
        print(f"\n📊 Estadísticas de la base de datos Railway:")
        print(f"   • Registros de cumplimiento: {cumplimiento_count}")
        print(f"   • Registros financieros: {financiero_count}")
        
        # Obtener datos de cumplimiento
        cumplimiento_data = db_manager.get_cumplimiento_data()
        if not cumplimiento_data.empty:
            print(f"\n📋 Datos de Cumplimiento (primeros 3 registros):")
            print(cumplimiento_data.head(3).to_string())
            
            # Mostrar filtros disponibles
            print(f"\n🔍 Filtros disponibles para Cumplimiento:")
            print(f"   • Secretarías: {sorted(cumplimiento_data['secretaria'].unique())}")
            print(f"   • Dependencias: {sorted(cumplimiento_data['dependencia'].unique())}")
            print(f"   • Sectores: {sorted(cumplimiento_data['sector'].unique())}")
            print(f"   • Programas: {sorted(cumplimiento_data['programa'].unique())}")
        
        # Obtener datos financieros
        financiero_data = db_manager.get_financiero_data()
        if not financiero_data.empty:
            print(f"\n💰 Datos Financieros (primeros 3 registros):")
            print(financiero_data.head(3).to_string())
            
            # Mostrar filtros disponibles
            print(f"\n🔍 Filtros disponibles para Financiero:")
            print(f"   • Dependencias: {sorted(financiero_data['dependencia'].unique())}")
            print(f"   • Sectores: {sorted(financiero_data['sector'].unique())}")
            print(f"   • Programas: {sorted(financiero_data['programa'].unique())}")
        
        # Calcular métricas
        if not cumplimiento_data.empty:
            avg_compliance = cumplimiento_data['porcentaje_cumplimiento'].mean()
            print(f"\n📈 Métricas de Cumplimiento:")
            print(f"   • Promedio de cumplimiento: {avg_compliance:.1f}%")
        
        if not financiero_data.empty:
            avg_execution = financiero_data['porcentaje_ejecucion'].mean()
            print(f"\n📈 Métricas Financieras:")
            print(f"   • Promedio de ejecución: {avg_execution:.1f}%")
        
        print(f"\n✅ Verificación completada exitosamente!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error verificando datos: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 Verificación de Datos - Railway")
    print("=" * 60)
    
    if verify_railway_data():
        print("\n🎉 ¡Los datos están correctamente cargados en Railway!")
    else:
        print("\n❌ Error en la verificación") 