import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Testa o endpoint de health check"""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_categoria(client: AsyncClient):
    """Testa criação de uma categoria"""
    categoria_data = {"nome": "Scale"}
    response = await client.post("/categorias/", json=categoria_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Scale"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_duplicate_categoria(client: AsyncClient):
    """Testa criação de categoria duplicada - deve retornar 303"""
    categoria_data = {"nome": "Scale"}
    
    # Primeira criação - sucesso
    response1 = await client.post("/categorias/", json=categoria_data)
    assert response1.status_code == 201
    
    # Segunda criação - erro 303
    response2 = await client.post("/categorias/", json=categoria_data)
    assert response2.status_code == 303
    assert "já existe" in response2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_list_categorias(client: AsyncClient):
    """Testa listagem de categorias"""
    # Criar duas categorias
    await client.post("/categorias/", json={"nome": "Scale"})
    await client.post("/categorias/", json={"nome": "RX"})
    
    # Listar
    response = await client.get("/categorias/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_create_centro_treinamento(client: AsyncClient):
    """Testa criação de um centro de treinamento"""
    centro_data = {
        "nome": "CT King",
        "endereco": "Rua X, Q02",
        "proprietario": "Marcos"
    }
    response = await client.post("/centros_treinamento/", json=centro_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "CT King"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_atleta(client: AsyncClient):
    """Testa criação de um atleta"""
    # Criar categoria e centro primeiro
    await client.post("/categorias/", json={"nome": "Scale"})
    await client.post("/centros_treinamento/", json={
        "nome": "CT King",
        "endereco": "Rua X",
        "proprietario": "Marcos"
    })
    
    # Criar atleta
    atleta_data = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "idade": 25,
        "peso": 75.5,
        "altura": 1.70,
        "sexo": "M",
        "categoria": {"nome": "Scale"},
        "centro_treinamento": {"nome": "CT King"}
    }
    
    response = await client.post("/atletas/", json=atleta_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["cpf"] == "12345678900"


@pytest.mark.asyncio
async def test_create_atleta_cpf_duplicado(client: AsyncClient):
    """Testa criação de atleta com CPF duplicado - deve retornar 303"""
    # Criar dependências
    await client.post("/categorias/", json={"nome": "Scale"})
    await client.post("/centros_treinamento/", json={
        "nome": "CT King",
        "endereco": "Rua X",
        "proprietario": "Marcos"
    })
    
    atleta_data = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "idade": 25,
        "peso": 75.5,
        "altura": 1.70,
        "sexo": "M",
        "categoria": {"nome": "Scale"},
        "centro_treinamento": {"nome": "CT King"}
    }
    
    # Primeira criação
    response1 = await client.post("/atletas/", json=atleta_data)
    assert response1.status_code == 201
    
    # Segunda criação com mesmo CPF
    atleta_data["nome"] = "Maria Santos"
    response2 = await client.post("/atletas/", json=atleta_data)
    assert response2.status_code == 303


@pytest.mark.asyncio
async def test_filter_atleta_by_nome(client: AsyncClient):
    """Testa filtro de atletas por nome"""
    # Criar dependências
    await client.post("/categorias/", json={"nome": "Scale"})
    await client.post("/centros_treinamento/", json={
        "nome": "CT King",
        "endereco": "Rua X",
        "proprietario": "Marcos"
    })
    
    # Criar atletas
    atleta1 = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "idade": 25,
        "peso": 75.5,
        "altura": 1.70,
        "sexo": "M",
        "categoria": {"nome": "Scale"},
        "centro_treinamento": {"nome": "CT King"}
    }
    atleta2 = {
        "nome": "Maria Santos",
        "cpf": "98765432100",
        "idade": 28,
        "peso": 62.0,
        "altura": 1.65,
        "sexo": "F",
        "categoria": {"nome": "Scale"},
        "centro_treinamento": {"nome": "CT King"}
    }
    
    await client.post("/atletas/", json=atleta1)
    await client.post("/atletas/", json=atleta2)
    
    # Filtrar por nome
    response = await client.get("/atletas/?nome=João")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("João" in item["nome"] for item in data["items"])


@pytest.mark.asyncio
async def test_atleta_get_all_custom_response(client: AsyncClient):
    """Testa que o GET all retorna apenas nome, categoria e centro_treinamento"""
    # Criar dependências
    await client.post("/categorias/", json={"nome": "Scale"})
    await client.post("/centros_treinamento/", json={
        "nome": "CT King",
        "endereco": "Rua X",
        "proprietario": "Marcos"
    })
    
    # Criar atleta
    atleta_data = {
        "nome": "João Silva",
        "cpf": "12345678900",
        "idade": 25,
        "peso": 75.5,
        "altura": 1.70,
        "sexo": "M",
        "categoria": {"nome": "Scale"},
        "centro_treinamento": {"nome": "CT King"}
    }
    await client.post("/atletas/", json=atleta_data)
    
    # Listar atletas
    response = await client.get("/atletas/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    
    # Verificar que retorna apenas os campos esperados
    if len(data["items"]) > 0:
        item = data["items"][0]
        assert "nome" in item
        assert "categoria" in item
        assert "centro_treinamento" in item
        # Não deve ter esses campos no GET all
        assert "cpf" not in item
        assert "idade" not in item
        assert "peso" not in item
