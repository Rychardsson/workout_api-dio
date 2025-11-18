# Guia de Setup Rápido - Windows PowerShell

## 1. Criar e Ativar Ambiente Virtual

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1
```

Se houver erro de execução de scripts, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 2. Instalar Dependências

```powershell
pip install -r requirements.txt
```

## 3. Subir o Banco de Dados

```powershell
docker-compose up -d
```

## 4. Criar e Aplicar Migrations

```powershell
# Criar migration
alembic revision --autogenerate -m "initial_migration"

# Aplicar migration
alembic upgrade head
```

## 5. Executar a API

```powershell
uvicorn workout_api.main:app --reload
```

## 6. Acessar a Documentação

Abra o navegador em: http://127.0.0.1:8000/docs

## Comandos Úteis

```powershell
# Parar o banco de dados
docker-compose down

# Ver logs do banco
docker-compose logs -f

# Verificar containers rodando
docker ps

# Reinstalar dependências
pip install -r requirements.txt --upgrade
```

## Testar a API

### 1. Criar Categoria
```powershell
curl -X POST "http://127.0.0.1:8000/categorias/" -H "Content-Type: application/json" -d '{\"nome\": \"Scale\"}'
```

### 2. Criar Centro de Treinamento
```powershell
curl -X POST "http://127.0.0.1:8000/centros_treinamento/" -H "Content-Type: application/json" -d '{\"nome\": \"CT King\", \"endereco\": \"Rua X, Q02\", \"proprietario\": \"Marcos\"}'
```

### 3. Criar Atleta
```powershell
curl -X POST "http://127.0.0.1:8000/atletas/" -H "Content-Type: application/json" -d '{\"nome\": \"João Silva\", \"cpf\": \"12345678900\", \"idade\": 25, \"peso\": 75.5, \"altura\": 1.70, \"sexo\": \"M\", \"categoria\": {\"nome\": \"Scale\"}, \"centro_treinamento\": {\"nome\": \"CT King\"}}'
```

### 4. Listar Atletas com Filtros
```powershell
# Todos os atletas
curl "http://127.0.0.1:8000/atletas/"

# Filtrar por nome
curl "http://127.0.0.1:8000/atletas/?nome=João"

# Filtrar por CPF
curl "http://127.0.0.1:8000/atletas/?cpf=12345678900"

# Com paginação
curl "http://127.0.0.1:8000/atletas/?page=1&size=10"
```

## Troubleshooting

### Erro de conexão com banco de dados
Verifique se o Docker está rodando:
```powershell
docker ps
```

### Erro de porta em uso
Verifique se a porta 5432 está disponível:
```powershell
netstat -ano | findstr :5432
```

### Erro de migration
Apague o banco e recrie:
```powershell
docker-compose down -v
docker-compose up -d
alembic upgrade head
```
