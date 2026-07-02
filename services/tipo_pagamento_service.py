from utils.validators import validate_nome
from repositories.tipo_pagamento_repository import TipoPagamentoRepository

class TipoPagamentoService:
    def __init__(self):
        self.repo = TipoPagamentoRepository()

    def create(self, user_id: str, nome: str) -> dict:
        """Criar novo tipo de pagamento"""
        valid_name, error = validate_nome(nome)
        if not valid_name:
            return {"success": False, "error": error}

        try:
            tipo = self.repo.create(user_id, nome)
            return {"success": True, "data": tipo}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_by_id(self, tipo_id: str) -> dict:
        """Obter tipo de pagamento por ID"""
        try:
            tipo = self.repo.get_by_id(tipo_id)
            if tipo:
                return {"success": True, "data": tipo}
            return {"success": False, "error": "Tipo de pagamento não encontrado"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_by_user(self, user_id: str) -> dict:
        """Listar tipos de pagamento do usuário"""
        try:
            tipos = self.repo.list_by_user(user_id)
            return {"success": True, "data": tipos}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(self, tipo_id: str, nome: str) -> dict:
        """Atualizar tipo de pagamento"""
        try:
            tipo = self.repo.update(tipo_id, nome)
            return {"success": True, "data": tipo}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, tipo_id: str) -> dict:
        """Deletar tipo de pagamento"""
        try:
            deleted = self.repo.delete(tipo_id)
            if deleted:
                return {"success": True, "message": "Tipo de pagamento deletado com sucesso"}
            return {"success": False, "error": "Erro ao deletar tipo de pagamento"}
        except Exception as e:
            return {"success": False, "error": str(e)}
