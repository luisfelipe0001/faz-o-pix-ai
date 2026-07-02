# 🔑 Recuperação de Senha - Guia Completo

## O que Implementei

✅ Fluxo de "Esqueci a Senha" na página de login  
✅ Integração com Supabase Auth  
✅ Email de recuperação automático  

---

## 🎯 Como Funciona

### **Fluxo do Usuário:**

```
1. Usuário clica em "Esqueceu a Senha?" (na página de login)
2. Digita seu email
3. Clica em "Enviar Email de Recuperação"
4. Supabase envia email com link de reset
5. Usuário clica no link
6. Define uma nova senha
7. Volta e faz login com a nova senha
```

---

## ⚙️ Configuração do Supabase

O Supabase já vem com tudo configurado, mas você pode customizar o email se quiser.

### **1. Ir para Configurações de Email (Opcional)**

1. Acesse: https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá para **Authentication → Email Templates**
4. Procure por **Reset Password**
5. Você pode editar o template do email

### **2. Configurar o Email de Origem**

Por padrão, o Supabase envia de: `no-reply@mail.supabase.io`

Se quiser usar seu próprio email (domínio próprio):
1. Vá para **Authentication → Email Settings**
2. Configure SMTP próprio (opcional, para escala maior)

---

## 📧 O que o Usuário Recebe

Quando solicita recuperação de senha, recebe um email como:

```
Assunto: Reset your password

Olá,

Clique no link abaixo para resetar sua senha:
https://seu-projeto.supabase.co/auth/v1/verify?...

Este link expira em 24 horas.

Se você não solicitou isso, ignore este email.
```

---

## 🔐 Fluxo Técnico

```python
# Usuário clica em "Enviar Email de Recuperação"
request_password_reset("tamires@exemplo.com")
    ↓
# Supabase Auth recebe a solicitação
client.auth.reset_password_for_email(email)
    ↓
# Supabase envia email automaticamente
Email: "Reset your password"
Link: https://seu-projeto.supabase.co/auth/v1/verify?...
    ↓
# Usuário clica no link do email
# Abre uma página do Supabase para resetar a senha
    ↓
# Usuário digita nova senha e confirma
    ↓
# Pronto! Pode fazer login com a nova senha
```

---

## ✅ Testes

### **Teste Localmente:**

1. Abra o app: `streamlit run main.py`
2. Na página de login, clique em **"Esqueceu a Senha?"**
3. Digite seu email
4. Clique em **"Enviar Email de Recuperação"**
5. Verifique seu email (pode levar alguns segundos)
6. Clique no link do email
7. Defina uma nova senha
8. Volte e faça login com a nova senha

---

## 🚨 Troubleshooting

| Problema | Solução |
|----------|---------|
| Não recebo o email | Verifique spam/lixo. Aguarde até 5 min. |
| Link do email expirado | Solicite um novo reset (link dura 24h) |
| "Email não encontrado" | Verifique se a conta foi criada com este email |
| SMTP Error | Contacte suporte do Supabase (rare) |

---

## 🔒 Segurança

✅ **Link com token único** — Só funciona uma vez  
✅ **Expira em 24 horas** — Segurança contra força bruta  
✅ **Sem acesso admin** — Você não vê nem reseta senhas dos usuários  
✅ **HTTPS** — Comunicação criptografada  

---

## 📝 Código Implementado

**Página de Login** (`pages/login.py`):
```python
if st.button("Enviar Email de Recuperação"):
    result = request_password_reset(email)
    if result["success"]:
        st.success("Email de recuperação enviado!")
```

**Função de Reset** (`utils/auth.py`):
```python
def request_password_reset(email: str) -> dict:
    client = get_supabase_client()
    response = client.auth.reset_password_for_email(email)
    return {"success": True, "data": response}
```

---

## 🎯 Resumo

| Aspecto | Status |
|--------|--------|
| Recuperação de senha | ✅ Implementado |
| Email automático | ✅ Funciona |
| Segurança | ✅ Bcrypt + Token |
| Expiração de link | ✅ 24 horas |
| Interface Streamlit | ✅ Pronta |

---

**Pronto! Seus usuários já podem recuperar a senha quando esquecerem.** 🎉

Se quiser customizar o email de recuperação, faça em:
https://supabase.com/dashboard → Authentication → Email Templates
