# WorkoutAPI

Esta é uma API de competição de crossfit chamada WorkoutAPI. É uma API desenvolvida com FastAPI que permite gerenciar atletas, categorias e centros de treinamento de forma assíncrona e escalável.

## Stack da API

A API foi desenvolvida utilizando:
- **FastAPI** (async)
- **SQLAlchemy** (ORM)
- **Alembic** (Migrations)
- **Pydantic** (Validação)
- **PostgreSQL** (Banco de dados)
- **fastapi-pagination** (Paginação)
- **Docker** (Containerização do banco de dados)

## Modelagem de Entidade e Relacionamento

A API possui 3 entidades principais:

- **Atleta**: Contém informações sobre os atletas (nome, cpf, idade, peso, altura, sexo)
- **Categoria**: Categorias dos atletas (ex: Scale, RX)
- **Centro de Treinamento**: Local onde o atleta treina

## Funcionalidades Implementadas

### Endpoints de Atleta
- ✅ POST `/atletas/` - Criar novo atleta
- ✅ GET `/atletas/` - Listar todos os atletas com paginação
  - Query parameters: `nome`, `cpf`
  - Retorno customizado: nome, centro_treinamento, categoria
  - Paginação com `limit` e `offset`
- ✅ GET `/atletas/{id}` - Buscar atleta por ID
- ✅ PATCH `/atletas/{id}` - Atualizar atleta
- ✅ DELETE `/atletas/{id}` - Deletar atleta

### Endpoints de Categoria
- ✅ POST `/categorias/` - Criar nova categoria
- ✅ GET `/categorias/` - Listar todas as categorias
- ✅ GET `/categorias/{id}` - Buscar categoria por ID

### Endpoints de Centro de Treinamento
- ✅ POST `/centros_treinamento/` - Criar novo centro
- ✅ GET `/centros_treinamento/` - Listar todos os centros
- ✅ GET `/centros_treinamento/{id}` - Buscar centro por ID

### Melhorias Implementadas 🎯

#### ✅ Validação Robusta
- **Validação de CPF completa** com algoritmo oficial brasileiro
- Validação de idade (1-149 anos)
- Validação de sexo (apenas 'M' ou 'F')
- Peso e altura com valores positivos

#### ✅ Sistema de Exception Handlers
- Tratamento global de erros
- Mensagens de erro padronizadas e descritivas
- Logging automático de exceções
- Status codes apropriados (303, 400, 404, 422, 500)

#### ✅ Logging Estruturado
- Logs com timestamp e níveis (INFO, WARNING, ERROR)
- Rastreamento de operações
- Facilita debugging e monitoramento

#### ✅ CORS Configurado
- Pronto para integração com frontends
- Configurável para ambientes de desenvolvimento e produção

#### ✅ Testes Automatizados
- **11 testes automatizados** cobrindo:
  - Health check
  - CRUD completo
  - Validações de duplicação
  - Filtros e paginação
  - Responses customizados
- Configuração com pytest e pytest-asyncio
- Suporte a cobertura de código

#### ✅ Documentação Aprimorada
- Descrições detalhadas em todos os endpoints
- Exemplos de uso no Swagger
- Documentação de validações e status codes
- Health check endpoint (`GET /`)

## Desafios Implementados

### 1. Query Parameters
- ✅ Filtro por **nome** do atleta
- ✅ Filtro por **CPF** do atleta

### 2. Response Customizado
- ✅ GET `/atletas/` retorna apenas: nome, centro_treinamento, categoria

### 3. Tratamento de Exceções
- ✅ Manipulação de `IntegrityError` para CPF duplicado
- ✅ Manipulação de `IntegrityError` para nomes duplicados em categorias e centros
- ✅ Status code **303** para duplicações
- ✅ Mensagem: "Já existe um atleta cadastrado com o cpf: x"

### 4. Paginação
- ✅ Implementado com `fastapi-pagination`
- ✅ Suporta `limit` e `offset` via query parameters

## Instalação e Execução

### Pré-requisitos
- Python 3.11.4+
- Docker e Docker Compose
- Make (opcional, para usar os comandos do Makefile)

### Passo 1: Configurar ambiente Python

Usando pyenv (recomendado):
```bash
pyenv virtualenv 3.11.4 workoutapi
pyenv activate workoutapi
```

Ou usando venv:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Passo 2: Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Subir o banco de dados

```bash
make run-docker
```

Ou usando docker-compose diretamente:
```bash
docker-compose up -d
```

### Passo 4: Criar as migrations

```bash
make create-migrations d="initial_migration"
```

### Passo 5: Aplicar as migrations

```bash
make run-migrations
```

### Passo 6: Executar a API

```bash
make run
```

Ou usando uvicorn diretamente:
```bash
uvicorn workout_api.main:app --reload
```

A API estará disponível em: **http://127.0.0.1:8000/docs**

## Exemplos de Uso

### 1. Criar uma Categoria

```bash
POST http://127.0.0.1:8000/categorias/
Content-Type: application/json

{
  "nome": "Scale"
}
```

### 2. Criar um Centro de Treinamento

```bash
POST http://127.0.0.1:8000/centros_treinamento/
Content-Type: application/json

{
  "nome": "CT King",
  "endereco": "Rua X, Q02",
  "proprietario": "Marcos"
}
```

### 3. Criar um Atleta

```bash
POST http://127.0.0.1:8000/atletas/
Content-Type: application/json

{
  "nome": "João Silva",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.70,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT King"
  }
}
```

### 4. Listar Atletas com Filtros e Paginação

```bash
GET http://127.0.0.1:8000/atletas/?nome=João&limit=10&page=1
```

### 5. Buscar Atleta por CPF

```bash
GET http://127.0.0.1:8000/atletas/?cpf=12345678900
```

## Comandos Úteis

### Makefile

```bash
make run-docker          # Subir o banco de dados
make stop-docker         # Parar o banco de dados
make create-migrations   # Criar nova migration
make run-migrations      # Aplicar migrations
make run                 # Executar a API
make test                # Executar testes
make test-cov            # Testes com cobertura de código
make install             # Instalar dependências
make install-dev         # Instalar dependências de desenvolvimento
make clean               # Limpar arquivos cache
```

### Alembic Manual

```bash
# Criar migration
alembic revision --autogenerate -m "nome_da_migration"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1
```

## Estrutura do Projeto

```
workout_api-dio/
├── workout_api/
│   ├── atleta/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── categorias/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── centro_treinamento/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── configs/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── settings.py
│   ├── contrib/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── __init__.py
│   └── main.py
├── .env
├── alembic.ini
├── docker-compose.yml
├── Makefile
├── README.md
└── requirements.txt
```

## Tecnologias e Conceitos Aplicados

- ✅ **Async/Await**: Operações assíncronas com SQLAlchemy
- ✅ **Dependency Injection**: FastAPI dependencies para sessão de banco
- ✅ **ORM**: SQLAlchemy 2.0 com mapped columns
- ✅ **Validação**: Pydantic v2 para validação de dados
- ✅ **Migrations**: Alembic para versionamento do schema
- ✅ **Paginação**: fastapi-pagination para resultados paginados
- ✅ **Exception Handling**: Tratamento customizado e global de erros
- ✅ **Query Parameters**: Filtros dinâmicos nos endpoints
- ✅ **Docker**: Containerização do PostgreSQL
- ✅ **API Documentation**: Swagger automático com FastAPI
- ✅ **Logging**: Sistema de logs estruturado
- ✅ **CORS**: Middleware para integração com frontends
- ✅ **Testes Automatizados**: Pytest com cobertura de código
- ✅ **Validadores Customizados**: Validação de CPF brasileira
- ✅ **Health Check**: Endpoint para monitoramento

## Configuração do Banco de Dados

As credenciais padrão do banco de dados estão definidas no arquivo `.env`:

```env
DATABASE_URL=postgresql+asyncpg://workout:workout@localhost:5432/workoutapi
```

Para alterar, edite o arquivo `.env` e o `docker-compose.yml` conforme necessário.

## Licença

Este projeto foi desenvolvido para fins educacionais.

---

## 📚 Documentação Adicional

- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Detalhes de todas as melhorias implementadas
- **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** - Checklist completo de implementação
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Visão geral do projeto
- **[SETUP_WINDOWS.md](SETUP_WINDOWS.md)** - Guia específico para Windows
- **[EXAMPLES.md](EXAMPLES.md)** - Exemplos de todas as requisições

## 🧪 Executar Testes

```bash
# Criar banco de teste
docker exec -it workout_api_db psql -U workout -c "CREATE DATABASE workoutapi_test;"

# Executar testes
pytest tests/ -v

# Com cobertura de código
pytest tests/ -v --cov=workout_api --cov-report=html
```
