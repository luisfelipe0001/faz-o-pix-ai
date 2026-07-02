from utils.validators import validate_nome, validate_email
from repositories.pessoa_repository import PessoaRepository
from typing import List

class PessoaService:
    def __init__(self):
        self.repo = PessoaRepository()

    def create(
        self,
        user_id: str,
        nome: str,
        email: str = None,
        telefone: str = None,
    ) -> dict:
        """Criar nova pessoa com validações"""
        valid_name, error = validate_nome(nome)
        if not valid_name:
            return {"success": False, "error": error}

        if email:
            valid_email, error = validate_email(email)
            if not valid_email:
                return {"success": False, "error": error}

        try:
            pessoa = self.repo.create(user_id, nome, email, telefone)
            return {"success": True, "data": pessoa}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_by_id(self, pessoa_id: str) -> dict:
        """Obter pessoa por ID"""
        try:
            pessoa = self.repo.get_by_id(pessoa_id)
            if pessoa:
                return {"success": True, "data": pessoa}
            return {"success": False, "error": "Pessoa não encontrada"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_by_user(self, user_id: str) -> dict:
        """Listar pessoas do usuário"""
        try:
            pessoas = self.repo.list_by_user(user_id)
            return {"success": True, "data": pessoas}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(
        self,
        pessoa_id: str,
        nome: str = None,
        email: str = None,
        telefone: str = None,
    ) -> dict:
        """Atualizar pessoa"""
        try:
            pessoa = self.repo.update(pessoa_id, nome, email, telefone)
            return {"success": True, "data": pessoa}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, pessoa_id: str) -> dict:
        """Deletar pessoa"""
        try:
            deleted = self.repo.delete(pessoa_id)
            if deleted:
                return {"success": True, "message": "Pessoa deletada com sucesso"}
            return {"success": False, "error": "Erro ao deletar pessoa"}
        except Exception as e:
            return {"success": False, "error": str(e)}
