"""
Configuración central leída desde el archivo .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:1234@localhost:5432/comidatienda"
)
