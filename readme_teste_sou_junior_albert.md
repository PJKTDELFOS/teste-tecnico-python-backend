# Performance Log API

Backend de um sistema de Log de Performance desenvolvido com FastAPI, PostgreSQL e SQLAlchemy.

## Sobre o Projeto

API para registro e diagnóstico de produtividade. O usuário registra sessões de trabalho,
cria tarefas com tipo e nível de foco, e ao final recebe um diagnóstico inteligente
baseado nos dados registrados.

## Stack

- Python 3.12
- FastAPI 0.136
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- JWT (python-jose)
- Passlib + bcrypt

## Como Rodar

### 1. Clone o repositório
```bash
git clone https://github.com/PJKTDELFOS/teste-tecnico-python-backend.git
cd teste-tecnico-python-backend
git checkout feature/performance-log-api
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Copie o arquivo de exemplo e preencha com seus dados:
```bash
cp .env-example .env
```

Conteúdo do `.env`:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Crie o banco de dados
```bash
psql -U postgres -c "CREATE DATABASE teste_backend;"
```

### 6. Rode as migrations
```bash
alembic upgrade head
```

### 7. Suba o servidor
```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Documentação

Acesse `http://localhost:8000/docs` para a documentação interativa Swagger.

> ⚠️ **Nota sobre o Swagger**: Os endpoints do grupo `tasks` estão sendo omitidos
> visualmente pelo Swagger devido a um conflito de paths entre os routers de tasks
> e comentarios que compartilham o mesmo prefix `/tasks`. A correção está sendo
> investigada. **Os endpoints funcionam corretamente** — apenas a exibição visual
> está afetada. Para verificar o funcionamento, utilize o TestClient ou ferramentas
> como Insomnia/Postman.
> 
> > ⚠️ **Nota sobre o Register pelo Swagger**: O endpoint `POST /auth/register` está
> retornando erro 500 quando chamado diretamente pelo Swagger UI. O problema está
> sendo investigado e tudo aponta para um conflito de versão do `bcrypt` com o
> processo do uvicorn — o servidor carrega o bcrypt antigo em memória mesmo após
> a atualização para a versão 4.0.1. **O endpoint funciona corretamente** quando
> testado via TestClient, Insomnia ou Postman. Para testar o register durante
> o desenvolvimento, utilize:
> ```bash
> python -c "
> from fastapi.testclient import TestClient
> from app.main import app
> client = TestClient(app)
> r = client.post('/auth/register', json={'name': 'seu_nome', 'email': 'seu@email.com', 'password': 'senha'})
> print(r.status_code, r.json())
> "
> ```

## Endpoints Disponíveis

### Auth
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/register` | Cadastro de usuário |
| POST | `/auth/login` | Login e geração de token JWT |

### Users
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/users/me` | Dados do usuário logado |
| PATCH | `/users/me` | Atualiza dados do usuário |
| DELETE | `/users/me` | Remove o usuário |
| GET | `/users/me/diagnostico-produtividade` | Diagnóstico inteligente |

### Sessions
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/sessions/` | Abre nova session |
| GET | `/sessions/` | Lista todas as sessions |
| GET | `/sessions/active` | Session ativa atual |
| POST | `/sessions/close` | Fecha a session ativa |
| GET | `/sessions/{id}` | Detalhe de uma session |

### Tasks
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/tasks/` | Cria uma task na session ativa |
| GET | `/tasks/` | Lista tasks da session ativa |
| GET | `/tasks/{id}` | Detalhe de uma task |
| PATCH | `/tasks/{id}/nivel-foco` | Atualiza nivel de foco |
| POST | `/tasks/{id}/close` | Fecha a task com nivel de foco |

### Comentarios
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/tasks/{id}/comentarios` | Adiciona comentario |
| GET | `/tasks/{id}/comentarios` | Lista comentarios |
| DELETE | `/tasks/{id}/comentarios/{id}` | Remove comentario |

## Fluxo de Uso