# ⚡ Quick Start - WorkoutAPI

## 🚀 Inicialização Rápida (5 minutos)

### 1️⃣ Setup Inicial
```powershell
# Clone ou navegue até o diretório
cd c:\Users\ResTIC16\Documents\workout_api-dio

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
.\venv\Scripts\Activate.ps1

# Instale as dependências
pip install -r requirements.txt
```

### 2️⃣ Banco de Dados
```powershell
# Suba o PostgreSQL
docker-compose up -d

# Aguarde 5 segundos para o banco inicializar
Start-Sleep -Seconds 5

# Crie a migration inicial
alembic revision --autogenerate -m "initial_migration"

# Aplique a migration
alembic upgrade head
```

### 3️⃣ Executar API
```powershell
uvicorn workout_api.main:app --reload
```

### 4️⃣ Testar
Abra o navegador em: **http://127.0.0.1:8000/docs**

---

## 🧪 Teste Completo dos Desafios

Execute estes comandos na ordem para testar todas as funcionalidades:

### 1. Criar Categoria
```powershell
curl.exe -X POST "http://127.0.0.1:8000/categorias/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "Scale"}'

curl.exe -X POST "http://127.0.0.1:8000/categorias/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "RX"}'
```

### 2. Criar Centro de Treinamento
```powershell
curl.exe -X POST "http://127.0.0.1:8000/centros_treinamento/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "CT King", "endereco": "Rua X, Q02", "proprietario": "Marcos"}'

curl.exe -X POST "http://127.0.0.1:8000/centros_treinamento/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "CrossFit Brasil", "endereco": "Av. Paulista, 1000", "proprietario": "Ana Silva"}'
```

### 3. Criar Atletas
```powershell
curl.exe -X POST "http://127.0.0.1:8000/atletas/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "João Silva", "cpf": "12345678900", "idade": 25, "peso": 75.5, "altura": 1.70, "sexo": "M", "categoria": {"nome": "Scale"}, "centro_treinamento": {"nome": "CT King"}}'

curl.exe -X POST "http://127.0.0.1:8000/atletas/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "Maria Santos", "cpf": "98765432100", "idade": 28, "peso": 62.3, "altura": 1.65, "sexo": "F", "categoria": {"nome": "RX"}, "centro_treinamento": {"nome": "CrossFit Brasil"}}'

curl.exe -X POST "http://127.0.0.1:8000/atletas/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "Pedro Oliveira", "cpf": "11122233344", "idade": 30, "peso": 82.0, "altura": 1.78, "sexo": "M", "categoria": {"nome": "RX"}, "centro_treinamento": {"nome": "CT King"}}'
```

### 4. Testar Query Parameters
```powershell
# Listar todos (response customizado)
curl.exe "http://127.0.0.1:8000/atletas/"

# Filtrar por nome
curl.exe "http://127.0.0.1:8000/atletas/?nome=João"

# Filtrar por CPF
curl.exe "http://127.0.0.1:8000/atletas/?cpf=12345678900"

# Filtrar por nome com paginação
curl.exe "http://127.0.0.1:8000/atletas/?nome=Silva&page=1&size=5"
```

### 5. Testar Exceção de Integridade (deve retornar 303)
```powershell
# Tentar criar atleta com CPF duplicado
curl.exe -X POST "http://127.0.0.1:8000/atletas/" `
  -H "Content-Type: application/json" `
  -d '{"nome": "Outro Nome", "cpf": "12345678900", "idade": 22, "peso": 70.0, "altura": 1.75, "sexo": "M", "categoria": {"nome": "Scale"}, "centro_treinamento": {"nome": "CT King"}}'
```

**Resposta esperada:**
```json
{
  "detail": "Já existe um atleta cadastrado com o cpf: 12345678900"
}
```

### 6. Testar Paginação
```powershell
# Página 1, 2 itens por página
curl.exe "http://127.0.0.1:8000/atletas/?page=1&size=2"

# Página 2
curl.exe "http://127.0.0.1:8000/atletas/?page=2&size=2"
```

---

## 📋 Checklist de Verificação

Execute este checklist para garantir que tudo está funcionando:

- [ ] PostgreSQL está rodando (`docker ps`)
- [ ] Ambiente virtual está ativado (`venv` no prompt)
- [ ] API está rodando (http://127.0.0.1:8000/docs acessível)
- [ ] Health check funciona (`GET /`)
- [ ] Consegue criar categorias
- [ ] Consegue criar centros de treinamento
- [ ] Consegue criar atletas
- [ ] Validação de CPF funciona (rejeita CPFs inválidos)
- [ ] Filtro por nome funciona (`?nome=João`)
- [ ] Filtro por CPF funciona (`?cpf=12345678900`)
- [ ] Response customizado em GET /atletas/ (só nome, categoria, centro)
- [ ] CPF duplicado retorna erro 303
- [ ] Paginação funciona (`?page=1&size=10`)
- [ ] Testes automatizados passam (`pytest tests/ -v`)
- [ ] Logs aparecem no console
- [ ] Documentação Swagger está completa

---

## 🔧 Comandos Úteis

### Banco de Dados
```powershell
# Ver status dos containers
docker ps

# Ver logs do PostgreSQL
docker-compose logs -f

# Parar banco
docker-compose down

# Limpar tudo e reiniciar
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### API
```powershell
# Executar API
uvicorn workout_api.main:app --reload

# Executar em outra porta
uvicorn workout_api.main:app --reload --port 8080

# Ver todas as rotas
uvicorn workout_api.main:app --reload --log-level debug
```

### Migrations
```powershell
# Ver status das migrations
alembic current

# Ver histórico
alembic history

# Criar nova migration
alembic revision --autogenerate -m "nome_da_migration"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1
```

### Desenvolvimento
```powershell
# Executar testes
pytest tests/ -v

# Testes com cobertura
pytest tests/ -v --cov=workout_api --cov-report=html

# Atualizar dependências
pip install --upgrade -r requirements.txt

# Congelar dependências atuais
pip freeze > requirements.txt

# Verificar dependências instaladas
pip list
```

---

## 🐛 Troubleshooting

### Erro: "Cannot connect to Docker daemon"
```powershell
# Verifique se o Docker Desktop está rodando
# Inicie o Docker Desktop manualmente
```

### Erro: "Port 5432 is already allocated"
```powershell
# Verifique se já existe um PostgreSQL rodando
netstat -ano | findstr :5432

# Pare o serviço conflitante ou use outra porta no docker-compose.yml
```

### Erro: "No module named 'workout_api'"
```powershell
# Certifique-se de estar no diretório correto
cd c:\Users\ResTIC16\Documents\workout_api-dio

# Certifique-se de que o ambiente virtual está ativado
.\venv\Scripts\Activate.ps1
```

### Erro: "Connection refused" ao acessar API
```powershell
# Verifique se a API está rodando
# Execute: uvicorn workout_api.main:app --reload
```

### Erro de Migration: "Target database is not up to date"
```powershell
# Aplique as migrations pendentes
alembic upgrade head
```

---

## 📊 Verificação Final

### Teste no Swagger (http://127.0.0.1:8000/docs)

1. **POST /categorias/** → Criar "Scale"
2. **POST /centros_treinamento/** → Criar "CT King"
3. **POST /atletas/** → Criar atleta
4. **GET /atletas/** → Ver response customizado
5. **GET /atletas/?nome=João** → Testar filtro
6. **GET /atletas/?page=1&size=5** → Testar paginação
7. **POST /atletas/** (mesmo CPF) → Ver erro 303

---

## ✅ Tudo Pronto!

Se todos os testes passaram, seu projeto está 100% funcional! 🎉

**Próximos passos:**
- Explore a API no Swagger
- Teste diferentes combinações de filtros
- Adicione mais atletas e teste a paginação
- Execute os testes automatizados (`pytest tests/ -v`)
- Experimente os diferentes endpoints
- Veja os logs no console

**Documentação completa:**
- **README.md** - Visão geral
- **IMPROVEMENTS.md** - Todas as melhorias implementadas
- **EXAMPLES.md** - Exemplos de requisições
- **IMPLEMENTATION_CHECKLIST.md** - Checklist completo
