from utils.db import get_supabase_client
from domain.user import User
from typing import Optional, List

class UserRepository:
    def __init__(self):
        self.client = get_supabase_client()
        self.table = "users"

    def create(self, user_id: str, email: str, full_name: str) -> User:
        """Criar novo usuário"""
        data = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
        }
        response = self.client.table(self.table).insert(data).execute()
        if response.data:
            return User(**response.data[0])
        raise Exception("Erro ao criar usuário")

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obter usuário por ID"""
        response = self.client.table(self.table).select("*").eq("id", user_id).execute()
        if response.data:
            return User(**response.data[0])
        return None

    def get_by_email(self, email: str) -> Optional[User]:
        """Obter usuário por email"""
        response = self.client.table(self.table).select("*").eq("email", email).execute()
        if response.data:
            return User(**response.data[0])
        return None

    def list_all(self) -> List[User]:
        """Listar todos os usuários"""
        response = self.client.table(self.table).select("*").execute()
        return [User(**row) for row in response.data]

    def delete(self, user_id: str) -> bool:
        """Deletar usuário"""
        response = self.client.table(self.table).delete().eq("id", user_id).execute()
        return len(response.data) > 0
