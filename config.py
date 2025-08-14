import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - Railway
# Railway proporciona automáticamente estas variables de entorno
DB_CONFIG = {
    'host': os.getenv('PGHOST', os.getenv('DB_HOST', 'localhost')),
    'port': os.getenv('PGPORT', os.getenv('DB_PORT', '5432')),
    'database': os.getenv('PGDATABASE', os.getenv('DB_NAME', 'railway')),
    'user': os.getenv('PGUSER', os.getenv('DB_USER', 'postgres')),
    'password': os.getenv('PGPASSWORD', os.getenv('DB_PASSWORD', 'postgres'))
}

# Database URL for SQLAlchemy
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}" 