# Exemplos de Requisições - WorkoutAPI

## Categorias

### Criar Categoria
```http
POST http://127.0.0.1:8000/categorias/
Content-Type: application/json

{
  "nome": "Scale"
}
```

### Criar Outra Categoria
```http
POST http://127.0.0.1:8000/categorias/
Content-Type: application/json

{
  "nome": "RX"
}
```

### Listar Todas as Categorias
```http
GET http://127.0.0.1:8000/categorias/
```

### Buscar Categoria por ID
```http
GET http://127.0.0.1:8000/categorias/1
```

### Teste de Duplicação (deve retornar erro 303)
```http
POST http://127.0.0.1:8000/categorias/
Content-Type: application/json

{
  "nome": "Scale"
}
```

## Centros de Treinamento

### Criar Centro de Treinamento
```http
POST http://127.0.0.1:8000/centros_treinamento/
Content-Type: application/json

{
  "nome": "CT King",
  "endereco": "Rua X, Q02",
  "proprietario": "Marcos"
}
```

### Criar Outro Centro
```http
POST http://127.0.0.1:8000/centros_treinamento/
Content-Type: application/json

{
  "nome": "CrossFit Brasil",
  "endereco": "Av. Paulista, 1000",
  "proprietario": "Ana Silva"
}
```

### Listar Todos os Centros
```http
GET http://127.0.0.1:8000/centros_treinamento/
```

### Buscar Centro por ID
```http
GET http://127.0.0.1:8000/centros_treinamento/1
```

### Teste de Duplicação (deve retornar erro 303)
```http
POST http://127.0.0.1:8000/centros_treinamento/
Content-Type: application/json

{
  "nome": "CT King",
  "endereco": "Outro endereço",
  "proprietario": "Outro dono"
}
```

## Atletas

### Criar Atleta 1
```http
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

### Criar Atleta 2
```http
POST http://127.0.0.1:8000/atletas/
Content-Type: application/json

{
  "nome": "Maria Santos",
  "cpf": "98765432100",
  "idade": 28,
  "peso": 62.3,
  "altura": 1.65,
  "sexo": "F",
  "categoria": {
    "nome": "RX"
  },
  "centro_treinamento": {
    "nome": "CrossFit Brasil"
  }
}
```

### Criar Atleta 3
```http
POST http://127.0.0.1:8000/atletas/
Content-Type: application/json

{
  "nome": "Pedro Oliveira",
  "cpf": "11122233344",
  "idade": 30,
  "peso": 82.0,
  "altura": 1.78,
  "sexo": "M",
  "categoria": {
    "nome": "RX"
  },
  "centro_treinamento": {
    "nome": "CT King"
  }
}
```

### Teste de CPF Duplicado (deve retornar erro 303)
```http
POST http://127.0.0.1:8000/atletas/
Content-Type: application/json

{
  "nome": "Outro Nome",
  "cpf": "12345678900",
  "idade": 22,
  "peso": 70.0,
  "altura": 1.75,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT King"
  }
}
```

### Listar Todos os Atletas (Resposta Customizada)
```http
GET http://127.0.0.1:8000/atletas/
```
**Retorno esperado**: Apenas nome, categoria e centro_treinamento

### Listar Atletas com Paginação
```http
GET http://127.0.0.1:8000/atletas/?page=1&size=2
```

### Filtrar Atletas por Nome
```http
GET http://127.0.0.1:8000/atletas/?nome=João
```

### Filtrar Atletas por Nome Parcial
```http
GET http://127.0.0.1:8000/atletas/?nome=Silva
```

### Filtrar Atletas por CPF
```http
GET http://127.0.0.1:8000/atletas/?cpf=12345678900
```

### Filtrar com Múltiplos Parâmetros
```http
GET http://127.0.0.1:8000/atletas/?nome=João&page=1&size=10
```

### Buscar Atleta por ID (Resposta Completa)
```http
GET http://127.0.0.1:8000/atletas/1
```

### Atualizar Atleta
```http
PATCH http://127.0.0.1:8000/atletas/1
Content-Type: application/json

{
  "nome": "João Silva Atualizado",
  "idade": 26
}
```

### Deletar Atleta
```http
DELETE http://127.0.0.1:8000/atletas/1
```

## Testes de Validação de Erros

### Categoria não encontrada
```http
POST http://127.0.0.1:8000/atletas/
Content-Type: application/json

{
  "nome": "Teste",
  "cpf": "00000000000",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.70,
  "sexo": "M",
  "categoria": {
    "nome": "Categoria Inexistente"
  },
  "centro_treinamento": {
    "nome": "CT King"
  }
}
```

### Centro de Treinamento não encontrado
```http
POST http://127.0.0.1:8000/atletas/
Content-Type: application/json

{
  "nome": "Teste",
  "cpf": "00000000000",
  "idade": 25,
  "peso": 75.5,
  "altura": 1.70,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "Centro Inexistente"
  }
}
```

### Atleta não encontrado
```http
GET http://127.0.0.1:8000/atletas/9999
```

## Respostas Esperadas

### Response Customizado - GET /atletas/
```json
{
  "items": [
    {
      "nome": "João Silva",
      "centro_treinamento": {
        "nome": "CT King"
      },
      "categoria": {
        "nome": "Scale"
      }
    }
  ],
  "total": 1,
  "page": 1,
  "size": 50,
  "pages": 1
}
```

### Response Completo - GET /atletas/{id}
```json
{
  "id": 1,
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
  },
  "created_at": "2025-11-18T12:00:00"
}
```

### Erro de CPF Duplicado (303)
```json
{
  "detail": "Já existe um atleta cadastrado com o cpf: 12345678900"
}
```

### Erro de Categoria Duplicada (303)
```json
{
  "detail": "Já existe uma categoria cadastrada com o nome: Scale"
}
```

### Erro de Centro Duplicado (303)
```json
{
  "detail": "Já existe um centro de treinamento cadastrado com o nome: CT King"
}
```
