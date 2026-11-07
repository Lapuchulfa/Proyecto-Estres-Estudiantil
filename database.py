import mysql.connector
from config import Config
import os

conexion =dict(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
)

# En la nube (Aiven) se usa SSL; en tu PC no
if Config.DB_HOST != "localhost":
    conexion["ssl_ca"] = os.path.join(os.path.dirname(__file__), "ca.pem")

def obtener_conexion():
    return mysql.connector.connect(**conexion)