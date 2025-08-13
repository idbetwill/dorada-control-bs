import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.cumplimiento_data = None
        self.financiero_data = None
    
    def load_cumplimiento_file(self, file_path):
        """Load the development plan compliance Excel file"""
        try:
            logger.info(f"Loading cumplimiento file: {file_path}")
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            logger.info(f"Found sheets: {excel_file.sheet_names}")
            
            # Look for the most relevant sheet for compliance data
            # Based on analysis, 'Hoja2' seems to have the compliance data
            target_sheet = None
            for sheet_name in excel_file.sheet_names:
                if 'Hoja2' in sheet_name:
                    target_sheet = sheet_name
                    break
            
            if target_sheet is None:
                # Try to find a sheet with compliance data
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    if 'CUMPLIMIENTO' in str(df.columns).upper():
                        target_sheet = sheet_name
                        break
            
            if target_sheet is None:
                # Use the first sheet as fallback
                target_sheet = excel_file.sheet_names[0]
            
            # Read the target sheet
            df = pd.read_excel(file_path, sheet_name=target_sheet)
            logger.info(f"Loaded data from sheet: {target_sheet}")
            logger.info(f"Data shape: {df.shape}")
            logger.info(f"Columns: {list(df.columns)}")
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Try to identify the correct column names based on actual data
            column_mapping = {}
            for col in df.columns:
                col_lower = str(col).lower()
                if 'sector' in col_lower and 'programa' in col_lower:
                    column_mapping[col] = 'Indicador'
                elif 'presupuesto' in col_lower and 'inicial' in col_lower:
                    column_mapping[col] = 'Meta Anual'
                elif 'presupuesto' in col_lower and 'definitivo' in col_lower:
                    column_mapping[col] = 'Avance Actual'
                elif 'cumplimiento' in col_lower or '%' in col_lower:
                    column_mapping[col] = '% Cumplimiento'
                elif 'obligado' in col_lower:
                    column_mapping[col] = 'Ejecutado'
            
            # Rename columns
            df = df.rename(columns=column_mapping)
            
            # Keep only relevant columns if they exist
            relevant_cols = ['Indicador', 'Meta Anual', 'Avance Actual', '% Cumplimiento', 'Ejecutado']
            available_cols = [col for col in relevant_cols if col in df.columns]
            
            if available_cols:
                df = df[available_cols]
                # Clean data - remove rows with all NaN values
                df = df.dropna(subset=['Indicador'])
                self.cumplimiento_data = df
                logger.info(f"Successfully loaded cumplimiento data with {len(df)} rows")
                return df
            else:
                logger.error("No relevant columns found in cumplimiento file")
                return None
                
        except Exception as e:
            logger.error(f"Error loading cumplimiento file: {e}")
            return None
    
    def load_financiero_file(self, file_path):
        """Load the financial report Excel file"""
        try:
            logger.info(f"Loading financiero file: {file_path}")
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            logger.info(f"Found sheets: {excel_file.sheet_names}")
            
            # Look for the most relevant sheet for financial data
            # Based on analysis, 'ejecución de gastos' seems to have the financial data
            target_sheet = None
            for sheet_name in excel_file.sheet_names:
                if 'ejecución de gastos' in sheet_name.lower():
                    target_sheet = sheet_name
                    break
            
            if target_sheet is None:
                # Try to find a sheet with financial data
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    if 'definitivo' in str(df.columns).lower() or 'pagos' in str(df.columns).lower():
                        target_sheet = sheet_name
                        break
            
            if target_sheet is None:
                # Use the first sheet as fallback
                target_sheet = excel_file.sheet_names[0]
            
            # Read the target sheet
            df = pd.read_excel(file_path, sheet_name=target_sheet)
            logger.info(f"Loaded data from sheet: {target_sheet}")
            logger.info(f"Data shape: {df.shape}")
            logger.info(f"Columns: {list(df.columns)}")
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Try to identify the correct column names based on actual data
            column_mapping = {}
            for col in df.columns:
                col_lower = str(col).lower()
                if 'rubro' in col_lower or 'concepto' in col_lower:
                    column_mapping[col] = 'Concepto'
                elif 'apropiacion' in col_lower and 'incial' in col_lower:
                    column_mapping[col] = 'Presupuesto Anual'
                elif 'definitivo' in col_lower:
                    column_mapping[col] = 'Presupuesto Definitivo'
                elif 'obligaciones' in col_lower:
                    column_mapping[col] = 'Ejecutado'
                elif 'disponibilidades' in col_lower:
                    column_mapping[col] = 'Disponible'
                elif 'pagos' in col_lower:
                    column_mapping[col] = 'Pagos'
                elif 'saldo' in col_lower and 'disponible' in col_lower:
                    column_mapping[col] = 'Saldo Disponible'
            
            # Rename columns
            df = df.rename(columns=column_mapping)
            
            # Keep only relevant columns if they exist
            relevant_cols = ['Concepto', 'Presupuesto Anual', 'Presupuesto Definitivo', 'Ejecutado', 'Disponible', 'Pagos']
            available_cols = [col for col in relevant_cols if col in df.columns]
            
            if available_cols:
                df = df[available_cols]
                # Clean data - remove rows with all NaN values
                df = df.dropna(subset=['Concepto'])
                # Calculate percentage execution if we have the data
                if 'Ejecutado' in df.columns and 'Presupuesto Definitivo' in df.columns:
                    df['% Ejecución'] = (df['Ejecutado'] / df['Presupuesto Definitivo'] * 100).fillna(0)
                
                self.financiero_data = df
                logger.info(f"Successfully loaded financiero data with {len(df)} rows")
                return df
            else:
                logger.error("No relevant columns found in financiero file")
                return None
                
        except Exception as e:
            logger.error(f"Error loading financiero file: {e}")
            return None
    
    def get_cumplimiento_data(self):
        """Get the loaded cumplimiento data"""
        return self.cumplimiento_data
    
    def get_financiero_data(self):
        """Get the loaded financiero data"""
        return self.financiero_data 