import re
from datetime import datetime

def validate_email(email: str) -> tuple[bool, str]:
    """Validar email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    return False, "Email inválido"

def validate_password(password: str) -> tuple[bool, str]:
    """Validar senha (mín 6 caracteres)"""
    if len(password) < 6:
        return False, "Senha deve ter no mínimo 6 caracteres"
    return True, ""

def validate_nome(nome: str) -> tuple[bool, str]:
    """Validar nome (não vazio)"""
    if not nome or len(nome.strip()) == 0:
        return False, "Nome não pode estar vazio"
    return True, ""

def validate_valor(valor: float) -> tuple[bool, str]:
    """Validar valor (maior que 0)"""
    if valor <= 0:
        return False, "Valor deve ser maior que 0"
    return True, ""

def validate_data(data_str: str) -> tuple[bool, str]:
    """Validar formato de data (YYYY-MM-DD)"""
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Data inválida. Use formato YYYY-MM-DD"

def validate_parcelas(qtd: int) -> tuple[bool, str]:
    """Validar quantidade de parcelas"""
    if qtd < 1:
        return False, "Parcelas deve ser pelo menos 1"
    return True, ""
