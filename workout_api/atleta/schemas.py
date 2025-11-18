from typing import Annotated, Optional
from pydantic import Field, PositiveFloat, BaseModel
from workout_api.categorias.schemas import CategoriaSimpleOut
from workout_api.centro_treinamento.schemas import CentroTreinamentoSimpleOut


class AtletaIn(BaseModel):
    nome: Annotated[str, Field(description='Nome do atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaSimpleOut, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoSimpleOut, Field(description='Centro de treinamento do atleta')]


class AtletaOut(AtletaIn):
    id: Annotated[int, Field(description='Identificador do atleta')]


class AtletaUpdate(BaseModel):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='João', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]


class AtletaGetAll(BaseModel):
    """Schema customizado para o endpoint get all de atletas"""
    nome: Annotated[str, Field(description='Nome do atleta', max_length=50)]
    centro_treinamento: Annotated[CentroTreinamentoSimpleOut, Field(description='Centro de treinamento')]
    categoria: Annotated[CategoriaSimpleOut, Field(description='Categoria')]
