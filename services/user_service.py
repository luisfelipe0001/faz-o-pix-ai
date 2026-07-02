from utils.validators import validate_email, validate_password, validate_nome
from utils.auth import register_user, login_user, logout_user, get_current_user
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, email: str, password: str, full_name: str) -> dict:
        """Registrar novo usuário com validações"""
        # Validações
        valid_email, error = validate_email(email)
        if not valid_email:
            return {"success": False, "error": error}

        valid_password, error = validate_password(password)
        if not valid_password:
            return {"success": False, "error": error}

        valid_name, error = validate_nome(full_name)
        if not valid_name:
            return {"success": False, "error": error}

        # Registrar no Supabase Auth
        auth_result = register_user(email, password, full_name)
        if not auth_result["success"]:
            return auth_result

        # Criar registro no banco
        try:
            user = self.repo.create(
                user_id=auth_result["data"].user.id,
                email=email,
                full_name=full_name,
            )
            return {"success": True, "data": user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login(self, email: str, password: str) -> dict:
        """Login do usuário"""
        result = login_user(email, password)
        if result["success"]:
            user_data = self.repo.get_by_id(result["data"].user.id)
            return {"success": True, "data": user_data}
        return result

    def logout(self) -> dict:
        """Logout do usuário"""
        return logout_user()

    def get_current_user(self) -> dict:
        """Obter usuário autenticado"""
        user = get_current_user()
        if user:
            user_data = self.repo.get_by_id(user.id)
            return {"success": True, "data": user_data}
        return {"success": False, "error": "Usuário não autenticado"}
