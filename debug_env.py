import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("DEBUG - Variáveis de Ambiente")
print("=" * 50)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
pwd = os.getenv("SUPABASE_DB_PASSWORD")

print(f"\nSUPABASE_URL: {url}")
print(f"SUPABASE_KEY: {key}")
print(f"SUPABASE_DB_PASSWORD: {pwd}")

print("\n" + "=" * 50)

if not url or not key:
    print("ERRO: Variáveis nao carregadas!")
else:
    print("OK: Variáveis carregadas corretamente!")

# Testar conexão
try:
    from supabase import create_client
    client = create_client(url, key)
    print("OK: Conexão com Supabase estabelecida!")
except Exception as e:
    print(f"ERRO ao conectar: {str(e)}")

print("=" * 50)
