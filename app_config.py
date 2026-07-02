import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")

# App Configuration
APP_NAME = os.getenv("APP_NAME", "Faz o Pix AI")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Validar se as variáveis obrigatórias estão definidas
def validate_config():
    required_vars = ["SUPABASE_URL", "SUPABASE_KEY", "SUPABASE_DB_PASSWORD"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise ValueError(
            f"Variáveis de ambiente faltando: {', '.join(missing)}. "
            f"Verifique o arquivo .env"
        )

validate_config()
