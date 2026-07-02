from supabase import create_client
import app_config

_client = None

def get_supabase_client():
    global _client
    if _client is None:
        _client = create_client(app_config.SUPABASE_URL, app_config.SUPABASE_KEY)
    return _client
