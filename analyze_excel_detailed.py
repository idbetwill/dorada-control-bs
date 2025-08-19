#!/usr/bin/env python3
"""
Script to analyze Excel files in detail
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_cumplimiento_file(file_path):
    """Analyze the compliance Excel file in detail"""
    try:
        logger.info(f"Analyzing cumplimiento file: {file_path}")
        
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        logger.info(f"Available sheets: {excel_file.sheet_names}")
        
        # Analyze each sheet to find the best data
        best_data = None
        best_sheet = None
        
        for sheet_name in excel_file.sheet_names:
            logger.info(f"Analyzing sheet: {sheet_name}")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Skip empty sheets
            if df.empty:
                continue
                
            logger.info(f"Sheet {sheet_name} shape: {df.shape}")
            logger.info(f"Columns: {list(df.columns)}")
            
            # Look for sheets with compliance data
            columns_str = str(df.columns).lower()
            if any(keyword in columns_str for keyword in ['cumplimiento', 'meta', 'avance', 'indicador']):
                logger.info(f"Found potential compliance data in sheet: {sheet_name}")
                
                # Clean the data
                df_clean = clean_cumplimiento_data(df, sheet_name)
                if df_clean is not None and len(df_clean) > 0:
                    best_data = df_clean
                    best_sheet = sheet_name
                    break
        
        if best_data is None:
            logger.warning("No suitable compliance data found")
            return None
            
        logger.info(f"Selected sheet: {best_sheet}")
        logger.info(f"Final data shape: {best_data.shape}")
        logger.info(f"Final columns: {list(best_data.columns)}")
        
        return best_data
        
    except Exception as e:
        logger.error(f"Error analyzing cumplimiento file: {e}")
        return None

def clean_cumplimiento_data(df, sheet_name):
    """Clean and structure compliance data"""
    try:
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Create a mapping based on the actual data structure
        column_mapping = {}
        
        for col in df.columns:
            col_str = str(col).lower()
            
            # Map indicator/program columns
            if any(keyword in col_str for keyword in ['sector', 'programa', 'indicador', 'meta']):
                if 'sector' in col_str and 'programa' in col_str:
                    column_mapping[col] = 'Indicador'
                elif 'indicador' in col_str:
                    column_mapping[col] = 'Indicador'
                elif 'meta' in col_str:
                    column_mapping[col] = 'Meta Anual'
            
            # Map budget columns
            elif 'presupuesto' in col_str:
                if 'inicial' in col_str:
                    column_mapping[col] = 'Presupuesto Inicial'
                elif 'definitivo' in col_str:
                    column_mapping[col] = 'Presupuesto Definitivo'
                elif 'obligado' in col_str:
                    column_mapping[col] = 'Presupuesto Obligado'
            
            # Map progress columns
            elif 'avance' in col_str:
                column_mapping[col] = 'Avance Actual'
            elif 'ejecutado' in col_str:
                column_mapping[col] = 'Ejecutado'
            
            # Map compliance percentage
            elif 'cumplimiento' in col_str or '%' in col_str:
                column_mapping[col] = '% Cumplimiento'
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Add missing columns with calculated values
        if 'Indicador' not in df.columns:
            # Try to find a suitable column for indicators
            for col in df.columns:
                if any(keyword in str(col).lower() for keyword in ['sector', 'programa', 'nombre']):
                    df['Indicador'] = df[col]
                    break
        
        # Calculate missing values
        if 'Meta Anual' in df.columns and 'Avance Actual' in df.columns:
            if '% Cumplimiento' not in df.columns:
                df['% Cumplimiento'] = (df['Avance Actual'] / df['Meta Anual'] * 100).fillna(0)
        
        # Clean data
        df = df.dropna(subset=['Indicador'])
        
        # Ensure we have the required columns
        required_cols = ['Indicador', '% Cumplimiento']
        available_cols = [col for col in required_cols if col in df.columns]
        
        if len(available_cols) >= 2:
            # Add default values for missing columns
            if 'Meta Anual' not in df.columns:
                df['Meta Anual'] = 100
            if 'Avance Actual' not in df.columns:
                df['Avance Actual'] = df['% Cumplimiento']
            if 'Presupuesto Inicial' not in df.columns:
                df['Presupuesto Inicial'] = 1000000
            if 'Presupuesto Definitivo' not in df.columns:
                df['Presupuesto Definitivo'] = df['Presupuesto Inicial']
            if 'Ejecutado' not in df.columns:
                df['Ejecutado'] = df['Presupuesto Definitivo'] * df['% Cumplimiento'] / 100
            
            return df
        
        return None
        
    except Exception as e:
        logger.error(f"Error cleaning compliance data: {e}")
        return None

def analyze_financiero_file(file_path):
    """Analyze the financial Excel file in detail"""
    try:
        logger.info(f"Analyzing financiero file: {file_path}")
        
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        logger.info(f"Available sheets: {excel_file.sheet_names}")
        
        # Analyze each sheet to find the best data
        best_data = None
        best_sheet = None
        
        for sheet_name in excel_file.sheet_names:
            logger.info(f"Analyzing sheet: {sheet_name}")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Skip empty sheets
            if df.empty:
                continue
                
            logger.info(f"Sheet {sheet_name} shape: {df.shape}")
            logger.info(f"Columns: {list(df.columns)}")
            
            # Look for sheets with financial data
            columns_str = str(df.columns).lower()
            if any(keyword in columns_str for keyword in ['presupuesto', 'ejecutado', 'pagos', 'definitivo']):
                logger.info(f"Found potential financial data in sheet: {sheet_name}")
                
                # Clean the data
                df_clean = clean_financiero_data(df, sheet_name)
                if df_clean is not None and len(df_clean) > 0:
                    best_data = df_clean
                    best_sheet = sheet_name
                    break
        
        if best_data is None:
            logger.warning("No suitable financial data found")
            return None
            
        logger.info(f"Selected sheet: {best_sheet}")
        logger.info(f"Final data shape: {best_data.shape}")
        logger.info(f"Final columns: {list(best_data.columns)}")
        
        return best_data
        
    except Exception as e:
        logger.error(f"Error analyzing financiero file: {e}")
        return None

def clean_financiero_data(df, sheet_name):
    """Clean and structure financial data"""
    try:
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Create a mapping based on the actual data structure
        column_mapping = {}
        
        for col in df.columns:
            col_str = str(col).lower()
            
            # Map concept/description columns
            if any(keyword in col_str for keyword in ['rubro', 'concepto', 'nombre', 'descripcion']):
                column_mapping[col] = 'Concepto'
            
            # Map budget columns
            elif 'presupuesto' in col_str:
                if 'inicial' in col_str or 'apropiacion' in col_str:
                    column_mapping[col] = 'Presupuesto Anual'
                elif 'definitivo' in col_str:
                    column_mapping[col] = 'Presupuesto Definitivo'
            
            # Map execution columns
            elif 'ejecutado' in col_str or 'obligaciones' in col_str:
                column_mapping[col] = 'Ejecutado'
            elif 'pagos' in col_str:
                column_mapping[col] = 'Pagos'
            elif 'disponibilidades' in col_str:
                column_mapping[col] = 'Disponible'
            elif 'saldo' in col_str and 'disponible' in col_str:
                column_mapping[col] = 'Saldo Disponible'
            
            # Map dependency/secretary columns
            elif 'dependencia' in col_str or 'secretaria' in col_str:
                column_mapping[col] = 'Dependencia'
            elif 'programa' in col_str:
                column_mapping[col] = 'Programa'
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Add missing columns with calculated values
        if 'Concepto' not in df.columns:
            # Try to find a suitable column for concepts
            for col in df.columns:
                if any(keyword in str(col).lower() for keyword in ['nombre', 'descripcion', 'rubro']):
                    df['Concepto'] = df[col]
                    break
        
        # Calculate missing values
        if 'Presupuesto Definitivo' in df.columns and 'Ejecutado' in df.columns:
            df['% Ejecución'] = (df['Ejecutado'] / df['Presupuesto Definitivo'] * 100).fillna(0)
        elif 'Presupuesto Anual' in df.columns and 'Ejecutado' in df.columns:
            df['% Ejecución'] = (df['Ejecutado'] / df['Presupuesto Anual'] * 100).fillna(0)
        
        # Calculate available amount
        if 'Presupuesto Definitivo' in df.columns and 'Ejecutado' in df.columns:
            df['Disponible'] = df['Presupuesto Definitivo'] - df['Ejecutado']
        
        # Clean data
        df = df.dropna(subset=['Concepto'])
        
        # Ensure we have the required columns
        required_cols = ['Concepto', '% Ejecución']
        available_cols = [col for col in required_cols if col in df.columns]
        
        if len(available_cols) >= 2:
            # Add default values for missing columns
            if 'Presupuesto Anual' not in df.columns:
                df['Presupuesto Anual'] = 1000000
            if 'Presupuesto Definitivo' not in df.columns:
                df['Presupuesto Definitivo'] = df['Presupuesto Anual']
            if 'Ejecutado' not in df.columns:
                df['Ejecutado'] = df['Presupuesto Definitivo'] * df['% Ejecución'] / 100
            if 'Disponible' not in df.columns:
                df['Disponible'] = df['Presupuesto Definitivo'] - df['Ejecutado']
            if 'Dependencia' not in df.columns:
                df['Dependencia'] = 'Secretaría General'
            if 'Programa' not in df.columns:
                df['Programa'] = 'Programa General'
            
            return df
        
        return None
        
    except Exception as e:
        logger.error(f"Error cleaning financial data: {e}")
        return None

def create_positive_sample_data():
    """Create sample data with positive progress for demonstration"""
    
    # Sample compliance data with positive progress
    cumplimiento_data = {
        'Indicador': [
            'Gestión del Territorio y Desarrollo Urbano',
            'Fomento Empresarial y Empleo',
            'Salud Integral y Bienestar',
            'Educación de Calidad',
            'Seguridad Ciudadana',
            'Cultura y Deporte',
            'Medio Ambiente Sostenible',
            'Infraestructura Vial',
            'Servicios Públicos',
            'Desarrollo Rural',
            'Tecnología e Innovación',
            'Participación Ciudadana',
            'Gobierno Digital',
            'Desarrollo Económico',
            'Inclusión Social'
        ],
        'Meta Anual': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        'Avance Actual': [85, 92, 78, 95, 88, 82, 90, 75, 87, 93, 80, 85, 91, 89, 86],
        '% Cumplimiento': [85, 92, 78, 95, 88, 82, 90, 75, 87, 93, 80, 85, 91, 89, 86],
        'Presupuesto Inicial': [500000000, 400000000, 300000000, 350000000, 250000000, 200000000, 180000000, 450000000, 320000000, 280000000, 150000000, 120000000, 100000000, 380000000, 220000000],
        'Presupuesto Definitivo': [520000000, 420000000, 310000000, 360000000, 260000000, 210000000, 185000000, 470000000, 330000000, 290000000, 155000000, 125000000, 105000000, 390000000, 225000000],
        'Ejecutado': [442000000, 386400000, 241800000, 342000000, 228800000, 172200000, 166500000, 352500000, 287100000, 269700000, 124000000, 106250000, 95550000, 347100000, 193500000],
        'Dependencia': [
            'Secretaría de Planeación',
            'Secretaría de Desarrollo Económico',
            'Secretaría de Salud',
            'Secretaría de Educación',
            'Secretaría de Gobierno',
            'Secretaría de Cultura',
            'Secretaría de Ambiente',
            'Secretaría de Obras Públicas',
            'Secretaría de Servicios Públicos',
            'Secretaría de Desarrollo Rural',
            'Secretaría de Tecnología',
            'Secretaría de Participación',
            'Secretaría de Gobierno Digital',
            'Secretaría de Desarrollo Económico',
            'Secretaría de Inclusión Social'
        ],
        'Programa': [
            'Gestión Territorial',
            'Fomento Empresarial',
            'Salud Pública',
            'Educación Básica',
            'Seguridad Ciudadana',
            'Cultura y Deporte',
            'Gestión Ambiental',
            'Infraestructura',
            'Servicios Públicos',
            'Desarrollo Rural',
            'Innovación Tecnológica',
            'Participación Ciudadana',
            'Gobierno Digital',
            'Desarrollo Económico',
            'Inclusión Social'
        ],
        'Eje': [
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 2: Desarrollo Social Inclusivo',
            'Eje 2: Desarrollo Social Inclusivo',
            'Eje 3: Seguridad y Convivencia',
            'Eje 2: Desarrollo Social Inclusivo',
            'Eje 4: Sostenibilidad Ambiental',
            'Eje 5: Infraestructura y Servicios',
            'Eje 5: Infraestructura y Servicios',
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 6: Gobierno Digital y Modernización',
            'Eje 3: Seguridad y Convivencia',
            'Eje 6: Gobierno Digital y Modernización',
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 2: Desarrollo Social Inclusivo'
        ]
    }
    
    # Sample financial data with positive execution
    financiero_data = {
        'Concepto': [
            'Gestión del Territorio',
            'Fomento Empresarial',
            'Salud Integral',
            'Educación de Calidad',
            'Seguridad Ciudadana',
            'Cultura y Deporte',
            'Medio Ambiente',
            'Infraestructura Vial',
            'Servicios Públicos',
            'Desarrollo Rural',
            'Tecnología e Innovación',
            'Participación Ciudadana',
            'Gobierno Digital',
            'Desarrollo Económico',
            'Inclusión Social'
        ],
        'Presupuesto Anual': [520000000, 420000000, 310000000, 360000000, 260000000, 210000000, 185000000, 470000000, 330000000, 290000000, 155000000, 125000000, 105000000, 390000000, 225000000],
        'Presupuesto Definitivo': [520000000, 420000000, 310000000, 360000000, 260000000, 210000000, 185000000, 470000000, 330000000, 290000000, 155000000, 125000000, 105000000, 390000000, 225000000],
        'Ejecutado': [442000000, 386400000, 241800000, 342000000, 228800000, 172200000, 166500000, 352500000, 287100000, 269700000, 124000000, 106250000, 95550000, 347100000, 193500000],
        'Disponible': [78000000, 33600000, 68200000, 18000000, 31200000, 37800000, 18500000, 117500000, 42900000, 20300000, 31000000, 18750000, 9450000, 42900000, 31500000],
        'Pagos': [420000000, 370000000, 230000000, 330000000, 220000000, 165000000, 160000000, 340000000, 280000000, 260000000, 120000000, 100000000, 90000000, 340000000, 185000000],
        '% Ejecución': [85.0, 92.0, 78.0, 95.0, 88.0, 82.0, 90.0, 75.0, 87.0, 93.0, 80.0, 85.0, 91.0, 89.0, 86.0],
        'Dependencia': [
            'Secretaría de Planeación',
            'Secretaría de Desarrollo Económico',
            'Secretaría de Salud',
            'Secretaría de Educación',
            'Secretaría de Gobierno',
            'Secretaría de Cultura',
            'Secretaría de Ambiente',
            'Secretaría de Obras Públicas',
            'Secretaría de Servicios Públicos',
            'Secretaría de Desarrollo Rural',
            'Secretaría de Tecnología',
            'Secretaría de Participación',
            'Secretaría de Gobierno Digital',
            'Secretaría de Desarrollo Económico',
            'Secretaría de Inclusión Social'
        ],
        'Programa': [
            'Gestión Territorial',
            'Fomento Empresarial',
            'Salud Pública',
            'Educación Básica',
            'Seguridad Ciudadana',
            'Cultura y Deporte',
            'Gestión Ambiental',
            'Infraestructura',
            'Servicios Públicos',
            'Desarrollo Rural',
            'Innovación Tecnológica',
            'Participación Ciudadana',
            'Gobierno Digital',
            'Desarrollo Económico',
            'Inclusión Social'
        ],
        'Eje': [
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 2: Desarrollo Social Inclusivo',
            'Eje 2: Desarrollo Social Inclusivo',
            'Eje 3: Seguridad y Convivencia',
            'Eje 2: Desarrollo Social Inclusivo',
            'Eje 4: Sostenibilidad Ambiental',
            'Eje 5: Infraestructura y Servicios',
            'Eje 5: Infraestructura y Servicios',
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 6: Gobierno Digital y Modernización',
            'Eje 3: Seguridad y Convivencia',
            'Eje 6: Gobierno Digital y Modernización',
            'Eje 1: Desarrollo Económico Sostenible',
            'Eje 2: Desarrollo Social Inclusivo'
        ]
    }
    
    return pd.DataFrame(cumplimiento_data), pd.DataFrame(financiero_data)

if __name__ == "__main__":
    # Analyze the actual Excel files
    cumplimiento_file = "% Cumplimiento 2025 Plan de Desarrollo.xlsx"
    financiero_file = "Reporte financiero 30 de junio 2025.xlsx"
    
    print("=== ANÁLISIS DETALLADO DE ARCHIVOS EXCEL ===")
    
    # Try to analyze actual files
    if Path(cumplimiento_file).exists():
        cumplimiento_data = analyze_cumplimiento_file(cumplimiento_file)
        if cumplimiento_data is not None:
            print(f"\n✅ Datos de cumplimiento cargados: {len(cumplimiento_data)} registros")
            print(f"Columnas: {list(cumplimiento_data.columns)}")
            print(f"Promedio de cumplimiento: {cumplimiento_data['% Cumplimiento'].mean():.1f}%")
        else:
            print("❌ No se pudieron cargar los datos de cumplimiento")
    else:
        print(f"❌ Archivo no encontrado: {cumplimiento_file}")
    
    if Path(financiero_file).exists():
        financiero_data = analyze_financiero_file(financiero_file)
        if financiero_data is not None:
            print(f"\n✅ Datos financieros cargados: {len(financiero_data)} registros")
            print(f"Columnas: {list(financiero_data.columns)}")
            print(f"Promedio de ejecución: {financiero_data['% Ejecución'].mean():.1f}%")
        else:
            print("❌ No se pudieron cargar los datos financieros")
    else:
        print(f"❌ Archivo no encontrado: {financiero_file}")
    
    # Create sample data with positive progress
    print("\n=== CREANDO DATOS DE MUESTRA CON AVANCE POSITIVO ===")
    cumplimiento_sample, financiero_sample = create_positive_sample_data()
    
    print(f"✅ Datos de cumplimiento de muestra: {len(cumplimiento_sample)} registros")
    print(f"Promedio de cumplimiento: {cumplimiento_sample['% Cumplimiento'].mean():.1f}%")
    
    print(f"✅ Datos financieros de muestra: {len(financiero_sample)} registros")
    print(f"Promedio de ejecución: {financiero_sample['% Ejecución'].mean():.1f}%")
    
    # Save sample data for use in the dashboard
    cumplimiento_sample.to_csv('cumplimiento_sample.csv', index=False)
    financiero_sample.to_csv('financiero_sample.csv', index=False)
    
    print("\n✅ Datos de muestra guardados para uso en el dashboard") 