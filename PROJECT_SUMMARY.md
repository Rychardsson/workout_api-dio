# 🏋️ WorkoutAPI - Projeto Completo

## 📌 Visão Geral

API assíncrona de competição de CrossFit desenvolvida com **FastAPI**, permitindo gerenciamento de atletas, categorias e centros de treinamento de forma eficiente e escalável.

---

## ✅ Status do Projeto

### 🎯 **TODOS OS REQUISITOS IMPLEMENTADOS!**

✅ API completa com FastAPI (async)  
✅ Banco de dados PostgreSQL com Docker  
✅ Migrations com Alembic  
✅ Validação com Pydantic v2  
✅ ORM com SQLAlchemy 2.0  
✅ **Query parameters (nome, cpf)**  
✅ **Response customizado no GET all**  
✅ **Tratamento de exceções de integridade (303)**  
✅ **Paginação com fastapi-pagination**  

---

## 📂 Estrutura do Projeto

```
workout_api-dio/
│
├── workout_api/                      # Pacote principal da API
│   ├── atleta/                       # Módulo de atletas
│   │   ├── __init__.py
│   │   ├── controller.py             # ✅ Rotas + Query params + Paginação
│   │   ├── models.py                 # ✅ Modelo SQLAlchemy
│   │   └── schemas.py                # ✅ Schemas Pydantic (AtletaGetAll)
│   │
│   ├── categorias/                   # Módulo de categorias
│   │   ├── __init__.py
│   │   ├── controller.py             # ✅ Rotas + Exceções
│   │   ├── models.py                 # ✅ Modelo SQLAlchemy
│   │   └── schemas.py                # ✅ Schemas Pydantic
│   │
│   ├── centro_treinamento/           # Módulo de centros de treinamento
│   │   ├── __init__.py
│   │   ├── controller.py             # ✅ Rotas + Exceções
│   │   ├── models.py                 # ✅ Modelo SQLAlchemy
│   │   └── schemas.py                # ✅ Schemas Pydantic
│   │
│   ├── configs/                      # Configurações
│   │   ├── __init__.py
│   │   ├── database.py               # ✅ AsyncSession + Dependency
│   │   └── settings.py               # ✅ Pydantic Settings
│   │
│   ├── contrib/                      # Componentes compartilhados
│   │   ├── __init__.py
│   │   └── models.py                 # ✅ BaseModel (DeclarativeBase)
│   │
│   ├── migrations/                   # Alembic migrations
│   │   ├── versions/                 # Arquivos de migration
│   │   ├── __init__.py
│   │   ├── env.py                    # ✅ Configuração Alembic
│   │   └── script.py.mako            # Template de migration
│   │
│   ├── __init__.py
│   └── main.py                       # ✅ FastAPI app + Routers + Pagination
│
├── .env                              # ✅ Variáveis de ambiente
├── .gitignore                        # ✅ Arquivos ignorados
├── alembic.ini                       # ✅ Configuração Alembic
├── docker-compose.yml                # ✅ PostgreSQL container
├── Makefile                          # ✅ Comandos auxiliares
├── requirements.txt                  # ✅ Dependências Python
│
├── README.md                         # 📖 Documentação principal
├── SETUP_WINDOWS.md                  # 📖 Guia para Windows
├── EXAMPLES.md                       # 📖 Exemplos de requisições
└── IMPLEMENTATION_CHECKLIST.md       # 📖 Checklist de implementação
```

---

## 🎯 Desafios Finais - Detalhamento

### 1️⃣ Query Parameters

**Endpoint:** `GET /atletas/`

**Parâmetros implementados:**
- `nome` (str, opcional) - Busca parcial no nome do atleta
- `cpf` (str, opcional) - Busca exata por CPF

**Exemplos:**
```bash
GET /atletas/?nome=João
GET /atletas/?cpf=12345678900
GET /atletas/?nome=Silva&page=1&size=10
```

**Código:**
```python
async def query(
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF"),
) -> Page[AtletaGetAll]:
    query = select(AtletaModel)
    if nome:
        query = query.filter(AtletaModel.nome.contains(nome))
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
```

---

### 2️⃣ Response Customizado

**Endpoint:** `GET /atletas/` (lista)

**Campos retornados:**
- ✅ nome
- ✅ centro_treinamento (apenas nome)
- ✅ categoria (apenas nome)

**Campos NÃO retornados:**
- ❌ id
- ❌ cpf
- ❌ idade
- ❌ peso
- ❌ altura
- ❌ sexo
- ❌ created_at

**Schema:**
```python
class AtletaGetAll(BaseModel):
    nome: str
    centro_treinamento: CentroTreinamentoSimpleOut
    categoria: CategoriaSimpleOut
```

**Response:**
```json
{
  "items": [
    {
      "nome": "João Silva",
      "centro_treinamento": {"nome": "CT King"},
      "categoria": {"nome": "Scale"}
    }
  ]
}
```

---

### 3️⃣ Exceções de Integridade

**Tabelas com tratamento:**
- ✅ Atletas (CPF único)
- ✅ Categorias (Nome único)
- ✅ Centros de Treinamento (Nome único)

**Status Code:** `303 SEE_OTHER`

**Mensagens:**
- Atleta: `"Já existe um atleta cadastrado com o cpf: {cpf}"`
- Categoria: `"Já existe uma categoria cadastrada com o nome: {nome}"`
- Centro: `"Já existe um centro de treinamento cadastrado com o nome: {nome}"`

**Código:**
```python
try:
    db_session.add(model)
    await db_session.commit()
except IntegrityError:
    await db_session.rollback()
    raise HTTPException(
        status_code=status.HTTP_303_SEE_OTHER,
        detail=f'Já existe um atleta cadastrado com o cpf: {cpf}'
    )
```

---

### 4️⃣ Paginação

**Biblioteca:** `fastapi-pagination==0.12.13`

**Parâmetros:**
- `page` (int, default=1) - Número da página
- `size` (int, default=50) - Itens por página

**Configuração:**
```python
# main.py
from fastapi_pagination import add_pagination
add_pagination(app)

# controller.py
from fastapi_pagination import Page, paginate

@router.get('/', response_model=Page[AtletaGetAll])
async def query(...) -> Page[AtletaGetAll]:
    return paginate(atletas_response)
```

**Response:**
```json
{
  "items": [...],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

**Exemplos:**
```bash
GET /atletas/?page=1&size=10
GET /atletas/?page=2&size=5
GET /atletas/?nome=João&page=1&size=20
```

---

## 🚀 Como Executar

### 1. Instalar Dependências
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Subir Banco de Dados
```powershell
docker-compose up -d
```

### 3. Criar e Aplicar Migrations
```powershell
alembic revision --autogenerate -m "initial_migration"
alembic upgrade head
```

### 4. Executar API
```powershell
uvicorn workout_api.main:app --reload
```

### 5. Acessar Documentação
```
http://127.0.0.1:8000/docs
```

---

## 📊 Endpoints Disponíveis

### Categorias
- `POST /categorias/` - Criar
- `GET /categorias/` - Listar todas
- `GET /categorias/{id}` - Buscar por ID

### Centros de Treinamento
- `POST /centros_treinamento/` - Criar
- `GET /centros_treinamento/` - Listar todos
- `GET /centros_treinamento/{id}` - Buscar por ID

### Atletas
- `POST /atletas/` - Criar
- `GET /atletas/` - Listar (customizado + paginação + filtros)
- `GET /atletas/{id}` - Buscar por ID (completo)
- `PATCH /atletas/{id}` - Atualizar
- `DELETE /atletas/{id}` - Deletar

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| FastAPI | 0.104.1 | Framework web assíncrono |
| SQLAlchemy | 2.0.23 | ORM |
| Alembic | 1.12.1 | Migrations |
| Pydantic | 2.5.0 | Validação de dados |
| PostgreSQL | 15 | Banco de dados |
| asyncpg | 0.29.0 | Driver PostgreSQL async |
| fastapi-pagination | 0.12.13 | Paginação |
| Uvicorn | 0.24.0 | ASGI server |
| Docker | - | Containerização |

---

## 📚 Documentação Adicional

- **README.md** - Documentação completa do projeto
- **SETUP_WINDOWS.md** - Guia específico para Windows PowerShell
- **EXAMPLES.md** - Exemplos de todas as requisições HTTP
- **IMPLEMENTATION_CHECKLIST.md** - Checklist detalhado de implementação

---

## ✨ Diferenciais Implementados

1. ✅ **Código modular** - Cada entidade em seu próprio módulo
2. ✅ **Async/Await** - Operações assíncronas em toda a aplicação
3. ✅ **Type hints** - Tipagem completa em Python
4. ✅ **Dependency Injection** - Injeção de dependências do FastAPI
5. ✅ **Exception Handling** - Tratamento robusto de erros
6. ✅ **Validação** - Pydantic para validação automática
7. ✅ **Documentação automática** - Swagger/OpenAPI
8. ✅ **Migrations** - Versionamento do banco de dados
9. ✅ **Docker** - Ambiente reproduzível
10. ✅ **Makefile** - Automação de comandos

---

## 🎓 Conceitos de Arquitetura

### Padrão de Camadas
```
Controller (Rotas)
    ↓
Schemas (Validação)
    ↓
Models (ORM)
    ↓
Database (PostgreSQL)
```

### Separação de Responsabilidades
- **Models**: Estrutura do banco de dados
- **Schemas**: Validação de entrada/saída
- **Controllers**: Lógica de negócio e rotas
- **Configs**: Configurações e conexões

---

## 🎉 Projeto Finalizado!

✅ Todos os requisitos implementados  
✅ Todos os desafios finais concluídos  
✅ Código limpo e bem documentado  
✅ Pronto para uso e aprendizado  

**Desenvolvido com ❤️ usando FastAPI e Python**
