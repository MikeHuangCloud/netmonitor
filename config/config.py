import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database type: 'mysql' or 'mssql'
    DB_TYPE = os.getenv('DB_TYPE', 'mysql')
    
    # MySQL 配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'netmonitor')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'netmonitor123')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'netmonitor')
    
    # Azure SQL 配置
    MSSQL_HOST = os.getenv('MSSQL_HOST', 'netmonitor-sqlserver.database.windows.net')
    MSSQL_PORT = int(os.getenv('MSSQL_PORT', 1433))
    MSSQL_USER = os.getenv('MSSQL_USER', 'netmonitoradmin')
    MSSQL_PASSWORD = os.getenv('MSSQL_PASSWORD', 'NetM0nitor@2026!')
    MSSQL_DATABASE = os.getenv('MSSQL_DATABASE', 'netmonitordb')
    
    # 根據 DB_TYPE 設定連接字串
    if DB_TYPE == 'mssql':
        # Azure SQL 連接字串
        SQLALCHEMY_DATABASE_URI = (
            f"mssql+pyodbc://{MSSQL_USER}:{quote_plus(MSSQL_PASSWORD)}@"
            f"{MSSQL_HOST}:{MSSQL_PORT}/{MSSQL_DATABASE}"
            f"?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
        )
    else:
        # MySQL 連接字串
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
            f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ping 配置
    PING_INTERVAL_SECONDS = int(os.getenv('PING_INTERVAL_SECONDS', 60))
    PING_COUNT = int(os.getenv('PING_COUNT', 4))
    PING_TIMEOUT = int(os.getenv('PING_TIMEOUT', 2))
    
    # 預設管理員帳號
    DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
    DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD', 'admin123')
