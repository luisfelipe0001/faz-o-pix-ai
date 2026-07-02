# 💰 Faz o Pix AI

Aplicação web para controlar empréstimos pessoais, acompanhar parcelas e nunca mais perder o controle de quem deve quanto.

## 🚀 Início Rápido

### 1. Clonar e Instalar Dependências

```bash
cd faz-o-pix-ai
pip install -r requirements.txt
```

### 2. Configurar Credenciais do Supabase

As credenciais já estão em `.env` (verificar se estão corretas):

```bash
cat .env
```

Deve conter:
```
SUPABASE_URL=https://...
SUPABASE_KEY=sb_...
SUPABASE_DB_PASSWORD=...
```

### 3. Criar as Tabelas no Supabase

**Via Dashboard Supabase:**

1. Acesse https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá para "SQL Editor" → "New Query"
4. Copie e execute cada arquivo em ordem:
   - `sql/ddl/001_create_users_table.sql`
   - `sql/ddl/002_create_pessoas_table.sql`
   - `sql/ddl/003_create_tipos_pagamento_table.sql`
   - `sql/ddl/004_create_emprestimos_table.sql`
   - `sql/ddl/005_create_parcelas_table.sql`

### 4. Rodar o App

```bash
streamlit run main.py
```

O app abrirá em `http://localhost:8501`

## 📱 Telas Disponíveis

1. **Login** — Autenticação e cadastro de usuários
2. **Dashboard** — Visão geral, dívidas próximas ao vencer
3. **Cadastro de Pessoas** — Quem você empresta dinheiro
4. **Tipos de Pagamento** — Crédito, débito, PIX, etc
5. **Gerenciar Dívidas** — CRUD completo + filtros + acompanhamento de parcelas

## 🏗️ Arquitetura

```
domain/        → Modelos de dados (User, Pessoa, Emprestimo, etc)
repositories/  → Acesso ao Supabase
services/      → Lógica de negócio
utils/         → Utilitários (auth, validação, formatação)
config/        → Configurações
pages/         → Telas Streamlit
sql/           → Scripts de criação de tabelas
```

## 🔐 Segurança

- Credenciais em `.env` (não commitado)
- Autenticação via Supabase Auth
- Isolamento por usuário (cada um vê só seus dados)

## 🚀 Funcionalidades

✅ Autenticação de usuários  
✅ Cadastro de pessoas/devedores  
✅ Cadastro de tipos de pagamento  
✅ Registro de empréstimos com parcelas automáticas  
✅ Acompanhamento de parcelas (pendente/recebida/atrasada)  
✅ Dashboard com resumos  
✅ Filtros por pessoa/status  
✅ Cálculo automático de saldo devedor  

## 📊 Fluxo de Dados

```
1. Usuário faz login
2. Cadastra pessoas (devedores)
3. Cadastra tipos de pagamento
4. Cria empréstimo
   → Sistema gera parcelas automaticamente
5. Acompanha parcelas no dashboard
6. Marca parcelas como recebidas
```

## 🛠️ Troubleshooting

### Erro: "Variáveis de ambiente faltando"
- Verifique se `.env` existe com as credenciais corretas

### Erro: "Table does not exist"
- Execute os scripts SQL em `sql/ddl/` no dashboard Supabase

### Erro ao fazer login
- Verifique se o usuário foi criado corretamente
- Confirme as credenciais do Supabase

## 📝 Desenvolvimento

Para adicionar novas funcionalidades:

1. **Model:** Adicione em `domain/`
2. **Repository:** Acesso ao Supabase em `repositories/`
3. **Service:** Lógica de negócio em `services/`
4. **Page:** Interface Streamlit em `pages/`

## 📞 Suporte

Qualquer dúvida, verifique:
- `SETUP.md` — Configuração de credenciais
- `sql/README.md` — Como criar tabelas
- Código nos comentários

---

**Desenvolvido com ❤️ usando Streamlit + Supabase**
