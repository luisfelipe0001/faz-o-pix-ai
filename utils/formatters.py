from datetime import datetime

def format_currency(valor: float) -> str:
    """Formatar valor para moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_date(data_str: str) -> str:
    """Formatar data de YYYY-MM-DD para DD/MM/YYYY"""
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except:
        return data_str

def format_date_reverse(data_str: str) -> str:
    """Formatar data de DD/MM/YYYY para YYYY-MM-DD"""
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        return data.strftime("%Y-%m-%d")
    except:
        return data_str

def get_status_badge(status: str) -> str:
    """Retornar emoji para status"""
    status_map = {
        "pendente": "⏳ Pendente",
        "recebida": "✅ Recebida",
        "atrasada": "⚠️ Atrasada",
        "em_andamento": "🔄 Em Andamento",
        "quitado": "✅ Quitado",
    }
    return status_map.get(status, status)
