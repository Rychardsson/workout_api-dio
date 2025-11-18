from typing import Annotated, Optional
from pydantic import Field, PositiveFloat, BaseModel, field_validator
from datetime import datetime
from workout_api.categorias.schemas import CategoriaSimpleOut
from workout_api.centro_treinamento.schemas import CentroTreinamentoSimpleOut
from workout_api.contrib.validators import validate_cpf


class AtletaIn(BaseModel):
    nome: Annotated[str, Field(description='Nome do atleta', example='João Silva', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=25, gt=0, lt=150)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta em kg', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta em metros', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta (M/F)', example='M', max_length=1, pattern='^[MF]$')]
    categoria: Annotated[CategoriaSimpleOut, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoSimpleOut, Field(description='Centro de treinamento do atleta')]
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf_format(cls, v: str) -> str:
        return validate_cpf(v)


class AtletaOut(AtletaIn):
    id: Annotated[int, Field(description='Identificador do atleta')]
    created_at: Annotated[datetime, Field(description='Data de criação do atleta')]


class AtletaUpdate(BaseModel):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='João', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]


class AtletaGetAll(BaseModel):
    """Schema customizado para o endpoint get all de atletas"""
    nome: Annotated[str, Field(description='Nome do atleta', max_length=50)]
    centro_treinamento: Annotated[CentroTreinamentoSimpleOut, Field(description='Centro de treinamento')]
    categoria: Annotated[CategoriaSimpleOut, Field(description='Categoria')]
