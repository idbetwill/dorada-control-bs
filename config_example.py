# Ejemplo de configuración para Dorada Dashboard
# Copia este archivo como config.py y modifica los valores según tu configuración

import os

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    'host': 'localhost',           # Host de PostgreSQL
    'port': '5432',               # Puerto de PostgreSQL
    'database': 'dorada_dashboard', # Nombre de la base de datos
    'user': 'postgres',           # Usuario de PostgreSQL
    'password': 'tu_password'     # Contraseña de PostgreSQL
}

# URL de la base de datos para SQLAlchemy
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Configuración del dashboard
DASHBOARD_CONFIG = {
    'title': 'Dorada Dashboard',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Configuración de archivos Excel
EXCEL_FILES = {
    'cumplimiento': '% Cumplimiento 2025 Plan de Desarrollo.xlsx',
    'financiero': 'Reporte financiero 30 de junio 2025.xlsx'
}

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
} 