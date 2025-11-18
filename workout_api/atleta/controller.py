from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException, Query
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, add_pagination, paginate
from typing import Optional

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaGetAll
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaSimpleOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoSimpleOut
from workout_api.configs.database import AsyncSession
from fastapi import Depends
from workout_api.configs.database import get_session

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
    description="""
    Cria um novo atleta no sistema.
    
    **Validações:**
    - CPF deve ser válido (11 dígitos numéricos com validação de dígitos verificadores)
    - CPF deve ser único no sistema
    - Categoria deve existir previamente
    - Centro de treinamento deve existir previamente
    - Idade deve ser entre 1 e 149 anos
    - Sexo deve ser 'M' ou 'F'
    - Peso e altura devem ser valores positivos
    
    **Retorna:**
    - Status 201: Atleta criado com sucesso
    - Status 303: CPF já cadastrado
    - Status 400: Categoria ou Centro de Treinamento não encontrados
    - Status 422: Dados de entrada inválidos
    """,
    responses={
        201: {"description": "Atleta criado com sucesso"},
        303: {"description": "CPF já cadastrado"},
        400: {"description": "Categoria ou Centro de Treinamento não encontrados"},
        422: {"description": "Dados de entrada inválidos"}
    }
)
async def post(
    db_session: AsyncSession = Depends(get_session),
    atleta_in: AtletaIn = Body(...),
) -> AtletaOut:
    # Buscar categoria
    categoria_nome = atleta_in.categoria.nome
    categoria = (
        await db_session.execute(
            select(CategoriaModel).filter_by(nome=categoria_nome)
        )
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Categoria {categoria_nome} não encontrada'
        )

    # Buscar centro de treinamento
    centro_nome = atleta_in.centro_treinamento.nome
    centro = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=centro_nome)
        )
    ).scalars().first()

    if not centro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Centro de treinamento {centro_nome} não encontrado'
        )

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

        return atleta_out
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}'
        )


@router.get(
    '/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaGetAll],
    description="""
    Lista todos os atletas cadastrados com suporte a filtros e paginação.
    
    **Filtros disponíveis:**
    - `nome`: Busca parcial por nome (case insensitive)
    - `cpf`: Busca exata por CPF
    
    **Paginação:**
    - `page`: Número da página (padrão: 1)
    - `size`: Itens por página (padrão: 50)
    
    **Resposta customizada:**
    Retorna apenas nome, categoria e centro de treinamento (sem CPF, idade, peso, etc.)
    
    **Exemplos:**
    - `/atletas/` - Lista todos
    - `/atletas/?nome=João` - Filtra por nome
    - `/atletas/?cpf=12345678900` - Busca por CPF
    - `/atletas/?page=1&size=10` - Paginação
    - `/atletas/?nome=Silva&page=2&size=5` - Filtro + paginação
    """,
    responses={
        200: {"description": "Lista de atletas retornada com sucesso"}
    }
)
async def query(
    db_session: AsyncSession = Depends(get_session),
    nome: Optional[str] = Query(None, description="Filtrar por nome do atleta"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF do atleta"),
) -> Page[AtletaGetAll]:
    query = select(AtletaModel)
    
    if nome:
        query = query.filter(AtletaModel.nome.contains(nome))
    
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    atletas = (await db_session.execute(query)).scalars().all()

    atletas_response = [
        AtletaGetAll(
            nome=atleta.nome,
            centro_treinamento=CentroTreinamentoSimpleOut(nome=atleta.centro_treinamento.nome),
            categoria=CategoriaSimpleOut(nome=atleta.categoria.nome)
        )
        for atleta in atletas
    ]

    return paginate(atletas_response)


@router.get(
    '/{id}',
    summary='Consultar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
    description="""
    Busca um atleta específico pelo ID.
    
    **Retorna:**
    Todos os dados do atleta, incluindo CPF, idade, peso, altura, etc.
    
    **Diferença do GET all:**
    Este endpoint retorna os dados completos do atleta,
    enquanto o GET /atletas/ retorna apenas nome, categoria e centro de treinamento.
    """,
    responses={
        200: {"description": "Atleta encontrado"},
        404: {"description": "Atleta não encontrado"}
    }
)
async def get(id: int, db_session: AsyncSession = Depends(get_session)) -> AtletaOut:
    atleta: AtletaModel = (
        await db_session.execute(select(AtletaModel).filter_by(pk_id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com id: {id}'
        )

    return AtletaOut(
        id=atleta.pk_id,
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        categoria=CategoriaSimpleOut(nome=atleta.categoria.nome),
        centro_treinamento=CentroTreinamentoSimpleOut(nome=atleta.centro_treinamento.nome),
        created_at=atleta.created_at
    )


@router.patch(
    '/{id}',
    summary='Atualizar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: int,
    db_session: AsyncSession = Depends(get_session),
    atleta_up: AtletaUpdate = Body(...),
) -> AtletaOut:
    atleta: AtletaModel = (
        await db_session.execute(select(AtletaModel).filter_by(pk_id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com id: {id}'
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut(
        id=atleta.pk_id,
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        categoria=CategoriaSimpleOut(nome=atleta.categoria.nome),
        centro_treinamento=CentroTreinamentoSimpleOut(nome=atleta.centro_treinamento.nome),
        created_at=atleta.created_at
    )


@router.delete(
    '/{id}',
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: int, db_session: AsyncSession = Depends(get_session)) -> None:
    atleta: AtletaModel = (
        await db_session.execute(select(AtletaModel).filter_by(pk_id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com id: {id}'
        )

    await db_session.delete(atleta)
    await db_session.commit()
