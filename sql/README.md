# Scripts SQL

Este diretório contém os scripts para criar as tabelas no Supabase.

## Como executar

### 1. Via Supabase Dashboard

1. Acesse https://supabase.com/dashboard
2. Selecione seu projeto
3. Vá para "SQL Editor"
4. Crie uma nova query
5. Copie o conteúdo de cada arquivo (começando por `001_create_users_table.sql`)
6. Execute em ordem

### 2. Via SQL Files (DDL)

Execute na ordem:
1. `ddl/001_create_users_table.sql`
2. `ddl/002_create_pessoas_table.sql`
3. `ddl/003_create_tipos_pagamento_table.sql`
4. `ddl/004_create_emprestimos_table.sql`
5. `ddl/005_create_parcelas_table.sql`

## Estrutura das Tabelas

- **users**: Usuários do sistema
- **pessoas**: Pessoas para quem você empresta dinheiro
- **tipos_pagamento**: Tipos de pagamento (Crédito, Débito, Pix, etc)
- **emprestimos**: Registro de empréstimos
- **parcelas**: Parcelas individuais de cada empréstimo
