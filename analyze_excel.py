import pandas as pd
import openpyxl
from pathlib import Path

def analyze_excel_file(file_path):
    """Analyze an Excel file and return information about its structure"""
    print(f"\n=== Analyzing {file_path} ===")
    
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        print(f"Number of sheets: {len(excel_file.sheet_names)}")
        print(f"Sheet names: {excel_file.sheet_names}")
        
        # Analyze each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"\n--- Sheet: {sheet_name} ---")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"First 5 rows:")
            print(df.head())
            print(f"Data types:")
            print(df.dtypes)
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    # Analyze both Excel files
    files = [
        "% Cumplimiento 2025 Plan de Desarrollo.xlsx",
        "Reporte financiero 30 de junio 2025.xlsx"
    ]
    
    for file_path in files:
        if Path(file_path).exists():
            analyze_excel_file(file_path)
        else:
            print(f"File {file_path} not found") 