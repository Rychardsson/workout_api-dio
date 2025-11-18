from typing import Annotated
from pydantic import Field, BaseModel


class CentroTreinamentoIn(BaseModel):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=50)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua X, Q02', max_length=60)]
    proprietario: Annotated[str, Field(description='Nome do proprietário', example='Marcos', max_length=30)]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[int, Field(description='Identificador do centro de treinamento')]


class CentroTreinamentoSimpleOut(BaseModel):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', max_length=50)]
