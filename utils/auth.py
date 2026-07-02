import streamlit as st
from utils.db import get_supabase_client

def register_user(email: str, password: str, full_name: str) -> dict:
    """Registrar novo usuário"""
    client = get_supabase_client()
    try:
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"full_name": full_name}
            }
        })
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email: str, password: str) -> dict:
    """Login do usuário"""
    client = get_supabase_client()
    try:
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

def logout_user():
    """Logout do usuário"""
    client = get_supabase_client()
    try:
        client.auth.sign_out()
        st.session_state.user = None
        st.session_state.authenticated = False
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_current_user():
    """Obter usuário autenticado"""
    client = get_supabase_client()
    try:
        session = client.auth.get_session()
        if session:
            return session.user
        return None
    except Exception:
        return None

def request_password_reset(email: str) -> dict:
    """Solicitar reset de senha por email"""
    client = get_supabase_client()
    try:
        response = client.auth.reset_password_for_email({"email": email})
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
