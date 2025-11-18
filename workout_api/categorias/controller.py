from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.configs.database import AsyncSession
from fastapi import Depends
from workout_api.configs.database import get_session

router = APIRouter()


@router.post(
    '/',
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: AsyncSession = Depends(get_session),
    categoria_in: CategoriaIn = Body(...),
) -> CategoriaOut:
    try:
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())

        db_session.add(categoria_model)
        await db_session.commit()
        
        return categoria_out
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma categoria cadastrada com o nome: {categoria_in.nome}'
        )


@router.get(
    '/',
    summary='Consultar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def query(db_session: AsyncSession = Depends(get_session)) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (
        await db_session.execute(select(CategoriaModel))
    ).scalars().all()

    return [CategoriaOut(id=categoria.pk_id, nome=categoria.nome) for categoria in categorias]


@router.get(
    '/{id}',
    summary='Consultar uma categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: int, db_session: AsyncSession = Depends(get_session)) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(pk_id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria não encontrada com id: {id}'
        )

    return CategoriaOut(id=categoria.pk_id, nome=categoria.nome)
