# 🔐 Configuração de Credenciais e Ambiente

## Estrutura de Segurança

Este projeto usa **variáveis de ambiente** para armazenar credenciais de forma segura.

### Arquivos

- **`.env`** — Arquivo local com suas credenciais (NÃO é versionado no Git)
- **`.env.example`** — Template mostrando o formato esperado (seguro fazer commit)
- **`config.py`** — Carrega automaticamente as variáveis de `.env`
- **`.gitignore`** — Previne que `.env` seja commitado

## Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. As Credenciais já estão em `.env`

O arquivo `.env` já foi criado com suas credenciais do Supabase. Verifique:

```bash
cat .env
```

### 3. Usar no seu App Streamlit

Importe e use assim:

```python
from config import SUPABASE_URL, SUPABASE_KEY

# Conectar ao Supabase
from supabase import create_client

client = create_client(SUPABASE_URL, SUPABASE_KEY)
```

## ⚠️ Segurança

- **Nunca commite o arquivo `.env`** — ele contém suas chaves secretas
- **Não compartilhe o `.env`** com outras pessoas
- Se vazarem as chaves, recrie-as no dashboard Supabase
- Para trabalhar com outras pessoas, cada um usa seu próprio `.env`

## Para Colaboradores

Se alguém novo vai trabalhar no projeto:

1. Clone o repositório
2. Copie `.env.example` para `.env`
3. Peça as credenciais reais do Supabase ao owner
4. Preencha o `.env` com as credenciais

```bash
cp .env.example .env
# Editar .env com as credenciais reais
```

## Referência Rápida

| Variável | Origem | Uso |
|----------|--------|-----|
| `SUPABASE_URL` | Dashboard Supabase → Settings → API | Conectar ao banco |
| `SUPABASE_KEY` | Dashboard Supabase → Settings → API → anon key | Autenticação pública |
| `SUPABASE_DB_PASSWORD` | Criado ao setup do projeto | Conexão direta ao banco (se necessário) |
