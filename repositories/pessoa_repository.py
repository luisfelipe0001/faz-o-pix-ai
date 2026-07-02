import uuid
from utils.db import get_supabase_client
from domain.pessoa import Pessoa
from typing import Optional, List

class PessoaRepository:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "pessoas"

    def create(self, user_id: str, nome: str, email: str = None, telefone: str = None) -> Pessoa:
        """Criar nova pessoa"""
        data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "nome": nome,
            "email": email,
            "telefone": telefone,
        }
        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return Pessoa(**response.data[0])
        raise Exception("Erro ao criar pessoa")

    def get_by_id(self, pessoa_id: str) -> Optional[Pessoa]:
        """Obter pessoa por ID"""
        response = self.client.table(self.table).select("*").eq("id", pessoa_id).execute()
        if response.data:
            return Pessoa(**response.data[0])
        return None

    def list_by_user(self, user_id: str) -> List[Pessoa]:
        """Listar pessoas do usuário"""
        response = self.client.table(self.table).select("*").eq("user_id", user_id).execute()
        return [Pessoa(**row) for row in response.data]

    def update(self, pessoa_id: str, nome: str = None, email: str = None, telefone: str = None) -> Pessoa:
        """Atualizar pessoa"""
        data = {}
        if nome:
            data["nome"] = nome
        if email:
            data["email"] = email
        if telefone:
            data["telefone"] = telefone

        response = self.client.table(self.table).update(data).eq("id", pessoa_id).execute()
        if response.data:
            return Pessoa(**response.data[0])
        raise Exception("Erro ao atualizar pessoa")

    def delete(self, pessoa_id: str) -> bool:
        """Deletar pessoa"""
        response = self.client.table(self.table).delete().eq("id", pessoa_id).execute()
        return len(response.data) > 0
