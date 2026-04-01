# SGI

Sistema de Gestão Integrado (MiniERP) - Backend API

## 🚀 Visão Geral

MiniERP é um sistema modular com arquitetura de Hub, onde cada módulo é plugável. Neste repositório, temos o backend implementado em FastAPI com persistência em PostgreSQL. O projeto oferece:

- Autenticação e autorização
- Estrutura de módulos (apps, auth, users, permissions)
- API REST com documentação automática

## 🛠️ Tecnologias

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy/SQLModel
- Uvicorn

## 🏃 Como executar localmente

Siga os passos abaixo a partir da raiz do repositório.

### 1. Clonar o repositório

```bash
git clone git@github.com:TyrGunllod/SGI.git
cd SGI
```

### 2. Configurar ambiente virtual

#### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

No seu terminal, dentro da pasta /backend, execute:

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` dentro de `backend/` com sua string de conexão:

```env
# Backend
DATABASE_URL=postgresql://postgres:senha@localhost:5432/database
SECRET_KEY=sua_chave
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Iniciar servidor

```bash
cd backend
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

## 📑 Documentação da API

Com o servidor em execução, acesse:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔌 Endpoints mais importantes

- `GET /apps` - Lista módulos disponíveis para o Hub
- `GET /health` - Verifica status da API e conexão com banco de dados

> Se houver autenticação configurada (JWT ou similar), siga os fluxos de login no módulo `auth` antes de acessar endpoints protegidos.

## 🗄️ Estrutura do projeto (backend)

```
backend/
  app/
    core/
      deps.py
      security.py
    internal/
      auth_middleware.py
      user.py
    modules/
      apps/
      auth/
      permissions/
      users/
  requirements.txt
```

## 🧪 Testes

- `backend/tests/seed.py` - scripts de seed para testes
- `backend/tests/test_conn.py` - teste de conexão com banco

## 💡 Observações

- Use `PSYCOPG2-BINARY` em ambiente local e `psycopg2` em produção se quiser controle fino de dependências.
- Centralize regras de negócio em `modules/*/service.py` e mantenha `controller.py` apenas como tradução de requisições/respostas.
