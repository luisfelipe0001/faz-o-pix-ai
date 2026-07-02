# 🚀 Melhorias Identificadas - Faz o Pix AI

**Data:** 01/07/2026  
**Status:** Planejamento para próximas sprints

---

## 📋 Melhorias por Prioridade

### 🔴 CRÍTICAS (Lógica de Negócio)

#### 1. **Vencimento Automático de Parcelas**
- **Problema:** Parcelas estão sendo geradas com data incrementando 30 dias a partir da data de compra
- **Desejado:** 
  - Por padrão, primeira parcela vence no dia 10 do mês seguinte
  - Campo de data customizável na criação da dívida para escolher outro dia se desejar
  - Exemplo: Se criar em 01/07, primeira parcela vence 10/08, segunda em 10/09, etc.
- **Status:** TODO
- **Arquivo:** `services/emprestimo_service.py` → método `_gerar_parcelas()`

#### 2. **Numeração de Parcelas (00/01 vs 01/02)**
- **Problema:** Algumas parcelas começam com 00, outras com 01
- **Desejado:** Sempre começar com 01/02 ou 01/10, nunca 00/XX
- **Status:** TODO
- **Arquivo:** `services/emprestimo_service.py` → método `_gerar_parcelas()`

#### 3. **Status de Dívida no Dashboard - Resumo por Pessoa**
- **Problema:** Quando marca uma parcela como paga/dívida como quitada, não atualiza no "Resumo por Pessoa"
- **Desejado:** Dashboard deve refletir status atual (paga/pendente/atrasada)
- **Status:** TODO
- **Arquivo:** `pages/home.py` → seção "Resumo por Pessoa"

---

### 🟡 ALTA PRIORIDADE (Dashboard)

#### 4. **Cards de Resumo - Atualização**
- **Problema:** Card "Total Recebido" não atualiza quando marca dívida como paga
- **Desejado:**
  - Card "Total Recebido" → soma todas as dívidas com status "quitado"
  - Novo card "Total Pendente" → soma parcelas/dívidas com status "pendente" ou "atrasada"
  - Manter "Total a Receber" (em_andamento)
- **Status:** TODO
- **Arquivo:** `pages/home.py` → seção "Cards de resumo"

#### 5. **Gráficos e Visualizações**
- **Problema:** Sem visualização gráfica dos dados
- **Desejado:** Adicionar gráficos com:
  - Dívidas por pessoa (gráfico de pizza)
  - Dívidas por tipo de pagamento (gráfico de barra)
  - Dívidas por cartão (gráfico de barra)
  - Linha do tempo: Valor total por mês (gráfico de linha)
  - Dispersão: Status das parcelas (gráfico de pizza - paga/pendente/atrasada)
- **Status:** TODO
- **Dependência:** Biblioteca Plotly ou Altair
- **Arquivo:** `pages/home.py` → nova seção "Análises e Gráficos"

#### 6. **Filtro de Data no Dashboard**
- **Problema:** Sem filtro por período
- **Desejado:**
  - Filtro "Período" para visualizar dívidas de data X a Y
  - Pré-configurados: "Este mês", "Últimos 30 dias", "Últimos 3 meses", "Customizar"
- **Status:** TODO
- **Arquivo:** `pages/home.py` → seção "Filtros"

---

### 🟢 MÉDIA PRIORIDADE (Funcionalidades Extras)

#### 7. **Alertas de Atraso**
- **Desejado:** Mostrar destaque para parcelas atrasadas
- **Status:** TODO
- **Arquivo:** `pages/home.py`

#### 8. **Relatório por Pessoa (Detalhe)**
- **Desejado:** Página separada com análise completa por pessoa
  - Total devendo
  - Parcelas pagas/pendentes
  - Próximo vencimento
  - Histórico de pagamentos
- **Status:** TODO
- **Arquivo:** Nova página `pages/relatorio_pessoa.py`

#### 9. **Exportar Dados**
- **Desejado:** Botão para exportar dívidas em Excel/PDF
- **Status:** TODO
- **Arquivo:** `pages/gerenciar_dividas.py`

#### 10. **Notificações/Alertas**
- **Desejado:** 
  - Alerta quando parcela está próxima de vencer
  - Alerta quando parcela vence
- **Status:** TODO
- **Arquivo:** `services/parcela_service.py`

---

## 🛠️ Mudanças Técnicas Necessárias

### Banco de Dados
- [ ] Adicionar campo `dia_vencimento` na tabela `emprestimos`

### Services
- [ ] Atualizar lógica de geração de parcelas em `emprestimo_service.py`
- [ ] Validar numeração de parcelas (sempre começar em 01)
- [ ] Criar método para calcular totais por status

### Pages
- [ ] Atualizar `home.py` com nova estrutura de cards
- [ ] Adicionar gráficos ao dashboard
- [ ] Implementar filtros de data
- [ ] Atualizar "Resumo por Pessoa" para refletir status correto

### Dependências Novas
```
plotly
openpyxl  # Para Excel
reportlab  # Para PDF
```

---

## 📊 Checklist para Próxima Sprint

- [ ] Corrigir vencimento automático de parcelas (dia 10 do mês)
- [ ] Corrigir numeração de parcelas (00 vs 01)
- [ ] Atualizar cards do dashboard
- [ ] Implementar gráficos básicos (4 principais)
- [ ] Adicionar filtro de data
- [ ] Testar fluxo completo com as mudanças

---

## 💡 Notas Adicionais

- Manter compatibilidade com dados já cadastrados
- Considerar migração de dados se houver mudanças estruturais
- Testar em múltiplos cenários (dívidas antigas, novas, quitadas)

---

**Próxima sessão:** Implementar itens de alta prioridade (4, 5, 6)
