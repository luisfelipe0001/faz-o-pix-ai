# Projeto: App de Controle de Empréstimos Pessoais

## 1. Visão Geral

Aplicação web pessoal para centralizar e controlar valores emprestados (dinheiro ou uso de cartão de crédito/débito) para familiares e pessoas próximas (mãe, irmã, pai, namorada, etc.), com acompanhamento de parcelas, vencimentos e status de recebimento.

**Objetivo principal:** nunca mais perder o controle de "quem me deve, quanto, e em qual parcela estamos".

**Formato:** aplicação web, com possibilidade futura de hospedagem e acesso via celular (responsivo).

---

## 2. Modelo de Dados

### 2.1 Tabela `pessoas`
Cadastro de quem recebe os empréstimos.

| Campo | Tipo | Descrição |
|---|---|---|
| id | int (PK) | Identificador único |
| nome | string | Nome da pessoa |
| email | string | Para referência/contato |
| telefone | string | Opcional |

### 2.2 Tabela `cartoes`
Cadastro dos cartões usados nos empréstimos (crédito ou débito).

| Campo | Tipo | Descrição |
|---|---|---|
| id | int (PK) | Identificador único |
| banco | string | Ex: Santander |
| final_digitos | string | Ex: 6442 |
| tipo | enum | `credito` / `debito` |
| dia_vencimento_fatura | int | Dia do mês em que a fatura vence (só p/ crédito) |

### 2.3 Tabela `tipos_pagamento`
Formas de pagamento possíveis no empréstimo.

| Campo | Tipo | Descrição |
|---|---|---|
| id | int (PK) | Identificador único |
| nome | string | Ex: Cartão de Crédito, Cartão de Débito, Dinheiro/Pix |

### 2.4 Tabela `emprestimos`
Registro de cada empréstimo feito.

| Campo | Tipo | Descrição |
|---|---|---|
| id | int (PK) | Identificador único |
| pessoa_id | FK → pessoas | Quem pegou emprestado |
| tipo_pagamento_id | FK → tipos_pagamento | Forma usada |
| cartao_id | FK → cartoes (nullable) | Preenchido se foi no cartão |
| descricao | string | Ex: "Compra Mercado Livre", "Loja física" |
| data_compra | date | Quando ocorreu a compra |
| valor_total | decimal | Valor total da dívida |
| qtd_parcelas | int | Em quantas vezes foi parcelado |
| status_geral | enum | `em_andamento` / `quitado` |

### 2.5 Tabela `parcelas`
Cada parcela individual gerada a partir de um empréstimo.

| Campo | Tipo | Descrição |
|---|---|---|
| id | int (PK) | Identificador único |
| emprestimo_id | FK → emprestimos | A qual empréstimo pertence |
| numero_parcela | int | Ex: 7 (de 10) |
| valor_parcela | decimal | Valor daquela parcela |
| data_vencimento | date | Calculada automaticamente |
| status | enum | `pendente` / `recebida` / `atrasada` |
| data_recebimento | date (nullable) | Preenchido quando você marca como recebida |

**Regra de negócio chave:** ao criar um empréstimo com `qtd_parcelas = 10`, o sistema gera automaticamente 10 registros em `parcelas`, com `data_vencimento` incrementando mês a mês a partir da `data_compra`. O app sempre sabe dizer "está na parcela 7 de 10" comparando a data atual com as datas de vencimento geradas.

---

## 3. Funcionalidades

### 3.1 Cadastros
- Cadastro de **pessoas** (nome, email, telefone)
- Cadastro de **cartões** (banco, final dos dígitos, tipo, dia de vencimento da fatura)
- Cadastro de **tipos de pagamento** (crédito, débito, dinheiro/pix)

### 3.2 Lançamento de empréstimo
Tela simples para lançar um novo empréstimo:
1. Selecionar pessoa (ou cadastrar nova na hora)
2. Selecionar tipo de pagamento
3. Se crédito/débito → selecionar qual cartão
4. Informar descrição da compra
5. Informar valor total e quantidade de parcelas
6. Sistema gera as parcelas automaticamente

### 3.3 Acompanhamento de parcelas
- Visualização por pessoa: quanto cada uma deve no total, e em qual parcela está cada dívida (ex: "parcela 7 de 10")
- Marcar parcela como recebida
- Status automático: pendente, atrasada (passou a data e não foi marcada) ou quitada (quando a última parcela é recebida)

### 3.4 Alertas de vencimento de cartão
Como cada cartão tem `dia_vencimento_fatura`, o sistema cruza:
- Quais parcelas de quais pessoas estão "dentro" da fatura que fecha em breve
- Gera um aviso do tipo: *"Fatura do Santander fecha dia 10 — você tem R$ 50 a cobrar da Tamires nessa fatura"*

Isso permite cobrar a pessoa **antes** do vencimento da fatura.

### 3.5 Relatório semanal automático (Google Apps Script)
Toda semana (ex: domingo à noite), um script dispara um e-mail para você mesmo contendo:
- **Resumo geral:** total a receber, total já recebido no mês, total de dívidas em aberto
- **Detalhamento por pessoa:** nome, valor devido, parcela atual (ex: "parcela 7 de 10"), próxima data de vencimento
- **Alertas de fatura:** cartões cuja fatura fecha nos próximos dias, com valores associados

**Por que Google Apps Script:** você já tem experiência com essa tecnologia (usada no site do escritório de advocacia), não exige servidor dedicado (diferente de uma solução via Airflow), e roda de forma agendada (trigger de tempo) direto na infraestrutura do Google.

**Fluxo técnico sugerido:**
1. Banco de dados (ex: Google Sheets, ou banco externo consultado via API) contém os dados de pessoas, empréstimos e parcelas
2. Script agendado (trigger semanal) lê os dados
3. Monta o HTML do e-mail com o resumo geral + detalhamento por pessoa
4. Dispara via `MailApp.sendEmail()` ou similar

---

## 4. Telas do App

1. **Dashboard principal:** visão consolidada — total a receber, dívidas por pessoa, alertas de fatura próxima
2. **Cadastro de Pessoas:** CRUD simples
3. **Cadastro de Cartões:** CRUD simples
4. **Cadastro de Tipos de Pagamento:** CRUD simples
5. **Novo Empréstimo:** formulário de lançamento (pessoa, tipo pagamento, cartão, descrição, valor, parcelas)
6. **Detalhe por Pessoa:** histórico completo, parcelas pagas e pendentes, progresso tipo "7 de 10"
7. **Configurações/Automação:** status do envio semanal de e-mail

---

## 5. Stack Sugerida

| Camada | Sugestão |
|---|---|
| Frontend | Streamlit (dado seu domínio da ferramenta) ou React simples |
| Backend/Dados | Banco relacional (SQLite/Postgres) ou Google Sheets como MVP inicial |
| Automação de e-mail | Google Apps Script (trigger semanal) |
| Hospedagem futura | Streamlit Community Cloud, ou VM simples, com acesso responsivo via celular |

**Sugestão de MVP:** começar com Google Sheets como "banco de dados" (rápido de montar, já compatível com Apps Script) e um app Streamlit simples para os cadastros e lançamentos. Depois, se crescer, migrar para banco relacional de verdade.

---

## 6. Próximos Passos

- [ ] Validar estrutura de dados (campos, nomes, tipos)
- [ ] Montar protótipo das telas (cadastro, lançamento, dashboard)
- [ ] Implementar geração automática de parcelas ao lançar empréstimo
- [ ] Implementar lógica de status (pendente/atrasada/recebida/quitada)
- [ ] Implementar cálculo de fatura por cartão
- [ ] Criar script no Google Apps Script para o e-mail semanal
- [ ] Testar fluxo completo ponta a ponta
- [ ] Avaliar hospedagem para acesso mobile