import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import logging
from config import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.connection = None
        
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.engine = create_engine(DATABASE_URL)
            self.connection = self.engine.connect()
            logger.info("Successfully connected to PostgreSQL database")
            return True
        except OperationalError as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    def create_tables(self):
        """Create necessary tables for the dashboard"""
        try:
            # Table for development plan compliance
            create_cumplimiento_table = """
            CREATE TABLE IF NOT EXISTS cumplimiento_plan_desarrollo (
                id SERIAL PRIMARY KEY,
                indicador VARCHAR(500),
                secretaria VARCHAR(200),
                dependencia VARCHAR(200),
                sector VARCHAR(200),
                programa VARCHAR(200),
                producto VARCHAR(200),
                meta_anual DECIMAL(15,2),
                avance_actual DECIMAL(15,2),
                porcentaje_cumplimiento DECIMAL(5,2),
                ejecutado DECIMAL(15,2),
                presupuesto_inicial DECIMAL(15,2),
                presupuesto_definitivo DECIMAL(15,2),
                fecha_actualizacion DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            # Table for financial report
            create_financiero_table = """
            CREATE TABLE IF NOT EXISTS reporte_financiero (
                id SERIAL PRIMARY KEY,
                concepto VARCHAR(500),
                dependencia VARCHAR(200),
                sector VARCHAR(200),
                programa VARCHAR(200),
                presupuesto_anual DECIMAL(15,2),
                presupuesto_definitivo DECIMAL(15,2),
                ejecutado DECIMAL(15,2),
                disponible DECIMAL(15,2),
                pagos DECIMAL(15,2),
                porcentaje_ejecucion DECIMAL(5,2),
                fecha_reporte DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            self.connection.execute(text(create_cumplimiento_table))
            self.connection.execute(text(create_financiero_table))
            self.connection.commit()
            logger.info("Tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
    
    def insert_cumplimiento_data(self, df):
        """Insert development plan compliance data"""
        try:
            # Clean and prepare data
            df_clean = df.copy()
            df_clean = df_clean.dropna(subset=['Indicador'])
            
            # Clear existing data
            self.connection.execute(text("DELETE FROM cumplimiento_plan_desarrollo"))
            
            # Insert data
            for _, row in df_clean.iterrows():
                insert_query = """
                INSERT INTO cumplimiento_plan_desarrollo 
                (indicador, secretaria, dependencia, sector, programa, producto, meta_anual, avance_actual, porcentaje_cumplimiento, ejecutado, presupuesto_inicial, presupuesto_definitivo, fecha_actualizacion)
                VALUES (:indicador, :secretaria, :dependencia, :sector, :programa, :producto, :meta_anual, :avance_actual, :porcentaje, :ejecutado, :presupuesto_inicial, :presupuesto_definitivo, :fecha)
                """
                
                # Extract values safely
                indicador = str(row.get('Indicador', ''))[:500]
                secretaria = str(row.get('Secretaría', 'Secretaría General'))[:200]
                dependencia = str(row.get('Dependencia', 'Dependencia General'))[:200]
                sector = str(row.get('Sector', 'Sector General'))[:200]
                programa = str(row.get('Programa', 'Programa General'))[:200]
                producto = str(row.get('Producto', 'Producto General'))[:200]
                meta_anual = float(row.get('Meta Anual', 0)) if pd.notna(row.get('Meta Anual')) else 0
                avance_actual = float(row.get('Avance Actual', 0)) if pd.notna(row.get('Avance Actual')) else 0
                porcentaje = float(row.get('% Cumplimiento', 0)) if pd.notna(row.get('% Cumplimiento')) else 0
                ejecutado = float(row.get('Ejecutado', 0)) if pd.notna(row.get('Ejecutado')) else 0
                presupuesto_inicial = float(row.get('Presupuesto Inicial', 0)) if pd.notna(row.get('Presupuesto Inicial')) else 0
                presupuesto_definitivo = float(row.get('Presupuesto Definitivo', 0)) if pd.notna(row.get('Presupuesto Definitivo')) else 0
                fecha = pd.Timestamp.now().date()
                
                self.connection.execute(text(insert_query), {
                    'indicador': indicador,
                    'secretaria': secretaria,
                    'dependencia': dependencia,
                    'sector': sector,
                    'programa': programa,
                    'producto': producto,
                    'meta_anual': meta_anual,
                    'avance_actual': avance_actual,
                    'porcentaje': porcentaje,
                    'ejecutado': ejecutado,
                    'presupuesto_inicial': presupuesto_inicial,
                    'presupuesto_definitivo': presupuesto_definitivo,
                    'fecha': fecha
                })
            
            self.connection.commit()
            logger.info(f"Inserted {len(df_clean)} records into cumplimiento_plan_desarrollo")
            
        except Exception as e:
            logger.error(f"Error inserting cumplimiento data: {e}")
    
    def insert_financiero_data(self, df):
        """Insert financial report data"""
        try:
            # Clean and prepare data
            df_clean = df.copy()
            df_clean = df_clean.dropna(subset=['Concepto'])
            
            # Clear existing data
            self.connection.execute(text("DELETE FROM reporte_financiero"))
            
            # Insert data
            for _, row in df_clean.iterrows():
                insert_query = """
                INSERT INTO reporte_financiero 
                (concepto, dependencia, sector, programa, presupuesto_anual, presupuesto_definitivo, ejecutado, disponible, pagos, porcentaje_ejecucion, fecha_reporte)
                VALUES (:concepto, :dependencia, :sector, :programa, :presupuesto_anual, :presupuesto_definitivo, :ejecutado, :disponible, :pagos, :porcentaje, :fecha)
                """
                
                # Extract values safely
                concepto = str(row.get('Concepto', ''))[:500]
                dependencia = str(row.get('Dependencia', 'Dependencia General'))[:200]
                sector = str(row.get('Sector', 'Sector General'))[:200]
                programa = str(row.get('Programa', 'Programa General'))[:200]
                presupuesto_anual = float(row.get('Presupuesto Anual', 0)) if pd.notna(row.get('Presupuesto Anual')) else 0
                presupuesto_definitivo = float(row.get('Presupuesto Definitivo', 0)) if pd.notna(row.get('Presupuesto Definitivo')) else 0
                ejecutado = float(row.get('Ejecutado', 0)) if pd.notna(row.get('Ejecutado')) else 0
                disponible = float(row.get('Disponible', 0)) if pd.notna(row.get('Disponible')) else 0
                pagos = float(row.get('Pagos', 0)) if pd.notna(row.get('Pagos')) else 0
                porcentaje = float(row.get('% Ejecución', 0)) if pd.notna(row.get('% Ejecución')) else 0
                fecha = pd.Timestamp.now().date()
                
                self.connection.execute(text(insert_query), {
                    'concepto': concepto,
                    'dependencia': dependencia,
                    'sector': sector,
                    'programa': programa,
                    'presupuesto_anual': presupuesto_anual,
                    'presupuesto_definitivo': presupuesto_definitivo,
                    'ejecutado': ejecutado,
                    'disponible': disponible,
                    'pagos': pagos,
                    'porcentaje': porcentaje,
                    'fecha': fecha
                })
            
            self.connection.commit()
            logger.info(f"Inserted {len(df_clean)} records into reporte_financiero")
            
        except Exception as e:
            logger.error(f"Error inserting financiero data: {e}")
    
    def get_cumplimiento_data(self):
        """Get all compliance data"""
        try:
            query = """
            SELECT 
                indicador, secretaria, dependencia, sector, programa, producto,
                meta_anual, avance_actual, porcentaje_cumplimiento, ejecutado,
                presupuesto_inicial, presupuesto_definitivo, fecha_actualizacion
            FROM cumplimiento_plan_desarrollo 
            ORDER BY created_at DESC
            """
            df = pd.read_sql(query, self.connection)
            return df
        except Exception as e:
            logger.error(f"Error getting cumplimiento data: {e}")
            return pd.DataFrame()
    
    def get_financiero_data(self):
        """Get all financial data"""
        try:
            query = """
            SELECT 
                concepto, dependencia, sector, programa,
                presupuesto_anual, presupuesto_definitivo, ejecutado, disponible, pagos, porcentaje_ejecucion, fecha_reporte
            FROM reporte_financiero 
            ORDER BY created_at DESC
            """
            df = pd.read_sql(query, self.connection)
            return df
        except Exception as e:
            logger.error(f"Error getting financiero data: {e}")
            return pd.DataFrame()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose() 