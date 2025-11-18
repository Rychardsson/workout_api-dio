from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.configs.database import AsyncSession
from fastapi import Depends
from workout_api.configs.database import get_session

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: AsyncSession = Depends(get_session),
    centro_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    try:
        centro_out = CentroTreinamentoOut(id=uuid4(), **centro_in.model_dump())
        centro_model = CentroTreinamentoModel(**centro_out.model_dump())

        db_session.add(centro_model)
        await db_session.commit()
        
        return centro_out
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um centro de treinamento cadastrado com o nome: {centro_in.nome}'
        )


@router.get(
    '/',
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: AsyncSession = Depends(get_session)) -> list[CentroTreinamentoOut]:
    centros: list[CentroTreinamentoOut] = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()

    return [
        CentroTreinamentoOut(
            id=centro.pk_id,
            nome=centro.nome,
            endereco=centro.endereco,
            proprietario=centro.proprietario
        )
        for centro in centros
    ]


@router.get(
    '/{id}',
    summary='Consultar um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: int, db_session: AsyncSession = Depends(get_session)) -> CentroTreinamentoOut:
    centro: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(pk_id=id))
    ).scalars().first()

    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado com id: {id}'
        )

    return CentroTreinamentoOut(
        id=centro.pk_id,
        nome=centro.nome,
        endereco=centro.endereco,
        proprietario=centro.proprietario
    )
